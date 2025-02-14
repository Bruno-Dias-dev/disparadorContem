from fastapi import APIRouter, HTTPException
from src.models.mensagem_model import MensagemModel
from src.models.grupo_mensagens_model import GrupoMensagensModel
from src.services.api_client import get_mensagens 
from src.services.mensagens_service import *

router = APIRouter()

@router.get("/tables/{table}/{page}/{qtd}", tags=["Listagem de Tabelas"])
def listar_tb_contratos(table: str, page: int, page_size: int):
    
    if not table:
        raise HTTPException(status_code=404, detail="Tabela não informada")
    
    result = list_tb(table=table, page=page, page_size=page_size)

    if isinstance(result, list):
        return {"data": [dict(row) for row in result]}
    else:
        return {"error": "Formato inesperado na resposta."}
    
# Rota para Mensagens
@router.get("/messages", response_model=MensagemModel, tags=["Mensagens"])
def listar_mensagens(page: int = 1, qtd: int = 50):
    return get_mensagens(page, qtd)

# Rota para Convênios
@router.get("/convenios", tags=["Convênios"])
def listar_convenios():
    return list_convenios()

@router.get("/tb-contratos/{page}/{qtd}", tags=["Tabela de Contratos"])
def listar_tb_contratos(page: int, page_size: int):
    result = list_tb_contratos(page=page, page_size=page_size)

    if isinstance(result, list):
        return {"data": [dict(row) for row in result]}
    else:
        return {"error": "Formato inesperado na resposta."}

@router.get("/tb-faturas", tags=["Tabela de Faturas"])
def listar_tb_contratos():
    return list_tb_faturas()

# Rota para Estipulantes
@router.get("/estipulantes", tags=["Estipulantes"])
def listar_estipulantes():
    return list_estipulantes()

# Rota para Status do Contrato
@router.get("/status-contrato", tags=["Status do Contrato"])
def listar_status_contrato():
    return list_status_contrato()

# Rota para Estipulantes
@router.get("/alerta-contrato", tags=["Alerta do Contrato"])
def listar_alerta_contrato():
    return list_alerta_contrato()

# Grupo de Mensagens
@router.post("/grupos", tags=["Grupos de Mensagens"])
def criar_grupo(grupo: GrupoMensagensModel):
    return create_grupo_mensagens(
        grupo.nome,
        grupo.convenios,
        grupo.estipulantes,
        grupo.status_contratos,
        grupo.alertas_contratos
    )
    
@router.get("/grupos", tags=["Grupos de Mensagens"])
def listar_grupos():
    return get_grupos_mensagens()

#  Buscar grupo por ID (GET)
@router.get("/grupos/{grupo_id}", tags=["Grupos de Mensagens"])
def buscar_grupo(grupo_id: int):
    grupo = get_grupo_by_id(grupo_id)
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    return grupo

#  Atualizar grupo (PUT)
@router.put("/grupos/{grupo_id}", tags=["Grupos de Mensagens"])
def atualizar_grupo(grupo_id: int, grupo: GrupoMensagensModel):
    grupo_existente = get_grupo_by_id(grupo_id)
    if not grupo_existente:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")

    return update_grupo_mensagens(
        grupo_id, grupo.nome, grupo.convenios, grupo.estipulantes, grupo.status_contratos, grupo.alertas_contratos
    )

#  Deletar grupo (DELETE)
@router.delete("/grupos/{grupo_id}", tags=["Grupos de Mensagens"])
def deletar_grupo(grupo_id: int):
    grupo_existente = get_grupo_by_id(grupo_id)
    if not grupo_existente:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")

    return delete_grupo_mensagens(grupo_id)