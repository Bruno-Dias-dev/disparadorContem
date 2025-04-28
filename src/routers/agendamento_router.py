from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from src.dependencies import *
from src.models.agendamento_model import AgendamentoModel
from src.services.agendamento_service import *
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="pages")

@router.post("/api/agendamentos", tags=["Agendamentos"])
def criar_agendamento_route(agendamento: AgendamentoModel):
    return criar_agendamento(
        agendamento.grupo_id,
        agendamento.horario_disparo,
        agendamento.ativo,
        str(agendamento.conexao_id),
        str(agendamento.departamento_id),
        agendamento.mensagem_ids
    )

@router.get("/api/agendamentos", tags=["Agendamentos"])
def listar_agendamentos_route(request: Request):
    return listar_agendamentos()    

@router.delete("/api/agendamento/{agendamento_id}", tags=["Agendamentos"])
def excluir_agendamento_route(
    agendamento_id: int,
):
    return excluir_agendamento(agendamento_id)


 