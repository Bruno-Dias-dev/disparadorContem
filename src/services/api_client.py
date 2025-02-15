import os
import requests
import time 
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BASE_URL_DIGITAL_SAC')
URI_LOGIN = 'oauth/token'

if not BASE_URL:
    raise ValueError("❌ ERRO: A variável BASE_URL_DIGITAL_SAC não está definida. Verifique o arquivo .env!")
else:
    print(f"ℹ️  BASE_URL: {BASE_URL}")

access_token = None
token_expires = None

def login():
    global access_token, token_expires
    data ={ 
        "grant_type": "password",
        "client_id": "api",
        "client_secret": "secret",
        "username": os.getenv('USERNAME_DIGITAL_SAC'), 
        "password": os.getenv('PASSWORD_DIGITAL_SAC')
    }
    request = requests.post(BASE_URL+URI_LOGIN, json = data)
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

def get_mensagens(page=1, qtd=50):
    """Consulta mensagens na API"""
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "page": str(page),
        "qtd": str(qtd),
    }
    url = BASE_URL + "/messages"
     
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}