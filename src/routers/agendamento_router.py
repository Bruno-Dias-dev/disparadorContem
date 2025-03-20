from fastapi import APIRouter, HTTPException
from src.models.agendamento_model import AgendamentoModel
from src.services.agendamento_service import *

router = APIRouter()

@router.post("/agendamentos", tags=["Agendamentos"])
def criar_agendamento_route(agendamento: AgendamentoModel):
    return criar_agendamento(
        agendamento.grupo_id,
        agendamento.horario_disparo,
        agendamento.ativo
    )

@router.get("/agendamentos", tags=["Agendamentos"])
def listar_agendamentos_route():
    return listar_agendamentos()

@router.delete("/agendamento/{agendamento_id}", tags=["Agendamentos"])
def excluir_agendamento_route(agendamento_id: int):
    return excluir_agendamento(agendamento_id)


 