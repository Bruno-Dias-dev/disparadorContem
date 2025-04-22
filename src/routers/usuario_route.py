from fastapi import APIRouter, Request, Form
from src.models.usuario_model import UsuarioCreate
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.services.usuario_service import cadastrar_usuario
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/usuarios")
templates = Jinja2Templates(directory="pages")

@router.get("/cadastrar", response_class=HTMLResponse)
async def form_usuario(request: Request):
    return templates.TemplateResponse("usuarios/cadastro.html", {"request": request})

@router.post("/cadastrar", response_class=HTMLResponse)
async def cadastrar_usuario_route(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...)
):
    usuario = UsuarioCreate(nome=nome, email=email, senha=senha, ativo=True)
    resultado = cadastrar_usuario(usuario)

    return templates.TemplateResponse("usuarios/cadastro.html", {
        "request": request,
        "mensagem": resultado.get("mensagem"),
        "erro": resultado.get("erro")
    })
