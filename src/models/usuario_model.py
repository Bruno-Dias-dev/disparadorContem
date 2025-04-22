from pydantic import BaseModel, EmailStr

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    ativo: bool = True

class UsuarioModel(BaseModel):
    id: int
    nome: str
    email: EmailStr
    senha: str
    ativo: bool = True
