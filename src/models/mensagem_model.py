from pydantic import BaseModel

class MensagemModel(BaseModel):
    mensagem: str
    ativo: bool = True
    titulo: str
   