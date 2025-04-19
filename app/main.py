# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import requests
import os

from . import models, schemas, database, auth
from .database import get_db

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


# -----------------------
# OAuth2 - Get Access Token
# -----------------------
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if auth.authenticate(form_data.username, form_data.password):
        return {"access_token": auth.ACCESS_TOKEN, "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


# Dependency to enforce auth on protected routes
def get_current_token(token: str = Depends(auth.oauth2_scheme)):
    if token != auth.ACCESS_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")


# -----------------------
# 1. GET /news: Fetch all news with pagination
# -----------------------
@app.get("/news", response_model=List[schemas.News])
def get_news(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), token: str = Depends(get_current_token)):
    return db.query(models.News).offset(skip).limit(limit).all()


# -----------------------
# 2. POST /news/save-latest: Save top 3 latest news to DB
# -----------------------
@app.post("/news/save-latest", status_code=201)
def save_latest_news(db: Session = Depends(get_db), token: str = Depends(get_current_token)):
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch news")

    news_items = response.json().get("articles", [])[:3]
    saved_news = []

    for item in news_items:
        news = models.News(
            title=item["title"],
            description=item["description"],
            url=item["url"],
            publishedAt=datetime.strptime(item["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
        )
        db.add(news)
        saved_news.append(news)

    db.commit()
    return {"message": f"Saved {len(saved_news)} latest news"}


# -----------------------
# 3. GET /news/headlines/country/{country_code}
# -----------------------
@app.get("/news/headlines/country/{country_code}")
def headlines_by_country(country_code: str, token: str = Depends(get_current_token)):
    url = f"https://newsapi.org/v2/top-headlines?country={country_code}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    return response.json()


# -----------------------
# 4. GET /news/headlines/source/{source_id}
# -----------------------
@app.get("/news/headlines/source/{source_id}")
def headlines_by_source(source_id: str, token: str = Depends(get_current_token)):
    url = f"https://newsapi.org/v2/top-headlines?sources={source_id}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    return response.json()


# -----------------------
# 5. GET /news/headlines/filter?country=xx&source=yy
# -----------------------
@app.get("/news/headlines/filter")
def headlines_filter(
    country: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    token: str = Depends(get_current_token)
):
    url = f"https://newsapi.org/v2/top-headlines?apiKey={NEWS_API_KEY}"
    if country:
        url += f"&country={country}"
    if source:
        url += f"&sources={source}"

    response = requests.get(url)
    return response.json()


# -----------------------
# Init DB tables on app startup
# -----------------------
@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=database.engine)
