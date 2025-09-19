# main.py
import os
from fastapi import FastAPI, APIRouter, Request, Response
from fastapi.templating import Jinja2Templates

app = FastAPI()
router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/config.js", tags=["config"])
async def get_config_js():
    # Lê a variável de ambiente ou usa um valor padrão
    api_url = os.environ.get("API_URL", "http://212.85.21.32:8000")

    # Cria o código JavaScript como uma string
    js_code = f"const API_URL = '{api_url}';"

    return Response(content=js_code, media_type="application/javascript")

@router.get("/componentes/navbar.html")
async def get_navbar(request: Request):
    return templates.TemplateResponse(request=request, name="navbar.html")


app.include_router(router)