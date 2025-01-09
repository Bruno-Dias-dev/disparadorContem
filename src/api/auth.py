import os
import requests
from dotenv import load_dotenv
import time

load_dotenv()
url = os.getenv('BASE_URL_DIGITAL_SAC')
URI_LOGIN = 'oauth/token'

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
 