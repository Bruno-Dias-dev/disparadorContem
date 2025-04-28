from src.utils.security import criptografar_senha
from config.conn import PostgresConnection
from src.models.usuario_model import UsuarioModel
from datetime import datetime

import os
from dotenv import load_dotenv
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "contem"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "C@med2024"),
    "port": int(os.getenv("DB_PORT", 5432)),
}

def get_db():
    db = PostgresConnection(**DB_CONFIG)
    db.connect()
    return db


def cadastrar_usuario(usuario: UsuarioModel, tags=["Usuário"]):
    db = get_db()
    try:
       # Verificar se o e-mail já existe
        query_check = "SELECT id FROM usuarios WHERE email = %s"
        existing = db.execute_query(query_check, (usuario.email,))
        if existing:
            return {"erro": "E-mail já cadastrado."} 

        senha_hash = criptografar_senha(usuario.senha)
        table = "usuarios"
        columns = ["nome", "email", "senha", "ativo", "created", "modified"]
        values = (usuario.nome, usuario.email, senha_hash, usuario.ativo, datetime.now(), datetime.now())
        
        db.insert_table(table=table, columns=columns, values=values)
        
        return {"mensagem": "Usuário cadastrado com sucesso!"}
    
    except Exception as e:
        print(f"Erro ao cadastrar dados: {e}")
        return {"error": str(e)}
    finally:
        db.close()
