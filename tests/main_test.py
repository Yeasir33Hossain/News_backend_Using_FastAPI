# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_token_generation():
    data = {
        'grant_type':'password',
        'username':'Yeasir',
        'password':'yeasir162#',
        
    }
    response = client.post("/token", data=data)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_news_unauthorized():
    response = client.get("/news")
    assert response.status_code == 401

def test_save_news_unauthorized():
    response = client.get("/news/save-latest")
    assert response.status_code == 401
