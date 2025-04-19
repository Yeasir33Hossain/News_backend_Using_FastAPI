# app/auth.py
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
ACCESS_TOKEN = "secure-token-123"  # Replace with real token logic if needed

def authenticate(client_id: str, client_secret: str):
    return client_id == CLIENT_ID and client_secret == CLIENT_SECRET
