from pydantic import BaseModel

class GrupoMensagensModel(BaseModel):
    nome: str
    convenios: dict = None
    estipulantes: dict = None
    status_contratos: dict = None
    alertas_contratos: dict = None