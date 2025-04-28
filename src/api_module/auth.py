import os
from config.conn import PostgresConnection
import requests
from dotenv import load_dotenv
import time
from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from fastapi import Request
from src.models.usuario_model import UsuarioModel as Usuario
from src.utils.security import verificar_senha
from sqlalchemy.orm import Session

router = APIRouter()

load_dotenv()
url = os.getenv('BASE_URL_DIGITAL_SAC')
URI_LOGIN = 'oauth/token'

access_token = None
token_expires = None

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": int(os.getenv("DB_PORT")),
}

def get_db():
    db = PostgresConnection(**DB_CONFIG)
    db.connect()
    return db


def login():
    global access_token, token_expires
    data ={ 
        "grant_type": "password",
        "client_id": "api",
        "client_secret": "secret",
        "username": os.getenv('USERNAME_DIGITAL_SAC'), 
        "password": os.getenv('PASSWORD_DIGITAL_SAC')
    }
    request = requests.post(url+URI_LOGIN, json = data)
    response_data = request.json()
    
    access_token = response_data.get('access_token')
    expires_in = response_data.get('expires_in')  # Tempo de expiração em segundos
    token_expires = time.time() + expires_in
    return access_token

def get_access_token():
    global access_token, token_expires
    
    if access_token is None or time.time() >= token_expires:
        access_token = login()
    return access_token

@router.post("/login", tags=["Usuário"]) 
async def login_default(request: Request, email: str = Form(...), senha: str = Form(...)):
    query = "SELECT * FROM usuarios WHERE email = %s"
    db = get_db()
    db.connect()
    
    usuario = db.execute_query(query, (email,))
    
    if not usuario:
        return RedirectResponse(url="/login?erro=1", status_code=status.HTTP_302_FOUND)

    usuario = usuario[0]

    if not verificar_senha(senha, usuario["senha"]):  # compara com hash do banco
        return RedirectResponse(url="/login?erro=1", status_code=status.HTTP_302_FOUND)

    request.session["user"] = {"id": usuario["id"], "email": usuario["email"]}
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)