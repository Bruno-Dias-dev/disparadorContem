from pydantic import BaseModel

class MensagemModel(BaseModel):
    mensagem: str
