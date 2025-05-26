from fastapi import APIRouter, HTTPException, UploadFile, File, status, Form
from src.models.mensagem_model import MensagemModel
from src.models.grupo_mensagens_model import GrupoMensagensModel
from src.services.api_client import get_mensagens 
from src.services.mensagens_service import *
from src.api_module.mensagens import get_conexoes_ativas, get_departamentos
import pandas as pd
import io

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
# @router.get("/messages", response_model=MensagemModel, tags=["Mensagens"])
# def listar_mensagens(page: int = 1, qtd: int = 50):
#     return get_mensagens(page, qtd)

@router.get("/mensagens", tags=["Mensagens"])
def listar_mensagens():
    return list_mensagens()

@router.post("/mensagens", tags=["Mensagens"])
def criar_mensagem(mensagem: MensagemModel):
    return create_mensagem(
        mensagem.mensagem,
        mensagem.ativo,
        mensagem.titulo,
)

@router.put("/mensagens/{mensagem_id}", tags=["Mensagens"])
def atualizar_mensagem(mensagem_id: int, mensagem: MensagemModel):
    msg_existente = get_msg_by_id(mensagem_id)
    if not msg_existente:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")

    return update_mensagens(
        mensagem_id,
        mensagem.mensagem,
        mensagem.ativo,
        mensagem.titulo,
    )   
    
@router.get("/mensagens/view/{mensagem_id}", tags=["Mensagens"])
def get_mensagem(mensagem_id: int):
    msg_existente = get_msg_by_id(mensagem_id)
    if not msg_existente:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    return msg_existente 

@router.delete("/mensagens/{mensagem_id}", tags=["Mensagens"])
def deletar_mensagem(mensagem_id: int):
    msg_existente = get_msg_by_id(mensagem_id)
    if not msg_existente:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")

    return delete_mensagem(mensagem_id)
    
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

# Rota para Uploads de Faturas
@router.post("/upload_faturas_excel", tags=["Faturas"])
async def upload_faturas_excel(
    file: UploadFile = File(...),
    grupo_id: int = Form(...),
    nome_grupo: str = Form(...)
    ):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Por favor, envie um arquivo .xlsx"
        )

    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))

        df.columns = [col.lower().strip() for col in df.columns]
        
        required_columns = ["fatura", "celular"]
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O arquivo deve conter as colunas: 'fatura', 'celular'."
            )

        faturas_para_inserir = []
        for index, row in df.iterrows():
            faturas_para_inserir.append({
                "codigo_da_fatura": str(row["fatura"]),
                "celular": str(row["celular"]),
                "nome": nome_grupo,
                "grupo_id": grupo_id
            })

        return insert_faturas_batch(faturas_para_inserir)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar o arquivo Excel: {str(e)}"
        )

# Grupo de Mensagens
@router.post("/grupos", tags=["Grupos de Mensagens"])
def criar_grupo(grupo: GrupoMensagensModel):
    return create_grupo_mensagens(
        grupo.nome,
        grupo.convenios,
        grupo.estipulantes,
        grupo.status_contratos,
        grupo.alertas_contratos,
        grupo.ativo,
        grupo.pdf,
        grupo.fase
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
        grupo_id, grupo.nome, grupo.convenios, grupo.estipulantes, grupo.status_contratos, grupo.alertas_contratos, grupo.ativo, grupo.pdf
    )

#  Deletar grupo (DELETE)
@router.delete("/grupos/{grupo_id}", tags=["Grupos de Mensagens"])
def deletar_grupo(grupo_id: int):
    grupo_existente = get_grupo_by_id(grupo_id)
    if not grupo_existente:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")

    return delete_grupo_mensagens(grupo_id)

@router.get("/grupos/{grupo_id}/faturas", tags=["Grupos de Mensagens"])
def listar_faturas_por_grupo(grupo_id: int):
    grupo = get_grupo_by_id(grupo_id)
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    
    faturas = get_faturas_por_grupo(grupo_id)
    return faturas

@router.get("/conexoes-ativas", tags=["Conexões Ativas"])
def listar_conexoes_ativas():
    return get_conexoes_ativas()

@router.get("/departamentos", tags=["Departamentos"])
def listar_departamentos():
    return get_departamentos()
