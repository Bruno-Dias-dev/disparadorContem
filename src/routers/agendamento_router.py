from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from src.dependencies import *
from src.models.agendamento_model import AgendamentoModel
from src.services.agendamento_service import *
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="pages")

@router.post("/agendamentos", tags=["Agendamentos"])
def criar_agendamento_route(
    agendamento: AgendamentoModel,
    usuario: str = Depends(verificar_usuario_logado)
):
    return criar_agendamento(
        agendamento.grupo_id,
        agendamento.horario_disparo,
        agendamento.ativo,
        str(agendamento.conexao_id),
        str(agendamento.departamento_id),
        agendamento.mensagem_ids
    )

@router.get("/agendamentos", tags=["Agendamentos"],response_class=HTMLResponse)
def listar_agendamentos_route(request: Request, usuario: str = Depends(verificar_usuario_logado)):
    agendamentos = listar_agendamentos()
    return templates.TemplateResponse("agendamentos/index.html", {
        "request": request, 
        "usuario": usuario,
        "agendamentos": agendamentos
    })

@router.delete("/agendamento/{agendamento_id}", tags=["Agendamentos"])
def excluir_agendamento_route(
    agendamento_id: int,
    usuario: str = Depends(verificar_usuario_logado)
):
    return excluir_agendamento(agendamento_id)


 