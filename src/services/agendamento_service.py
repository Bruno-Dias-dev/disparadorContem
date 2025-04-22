from config.conn import PostgresConnection
import os
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import pytz

# Define o fuso horário correto
tz = pytz.timezone("America/Sao_Paulo")

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": int(os.getenv("DB_PORT")),
}

def get_db():
    db = PostgresConnection(**DB_CONFIG)
    db.connect()
    return db

def criar_agendamento(grupo_id, horario_disparo, ativo, conexao_id, departamento_id, mensagem_ids=None,):
    """Cria um novo agendamento de mensagem"""
    db = PostgresConnection(**DB_CONFIG)
    db.connect()
    try:
        now = datetime.now(tz)
        if isinstance(horario_disparo, str):
            horario_disparo = datetime.fromisoformat(horario_disparo.replace("Z", "+00:00"))
        
        horario_disparo = horario_disparo.astimezone(tz) 
      
        if horario_disparo < now:
            return {"error": "A data/hora de agendamento deve ser no futuro."}

        db.insert_table(table="agendamentos", columns=("grupo_id", "horario_disparo", "ativo", "mensagem_ids", "conexao_id", "departamento_id"), values=(grupo_id, horario_disparo, ativo, mensagem_ids,str(conexao_id), str(departamento_id)))
        return { "message": "Agendamento criado com sucesso"}
    except Exception as e:
        print("❌ Erro ao criar agendamento:", e)
        return {"error": str(e)}
    finally:
        db.close()

def listar_agendamentos():
    """Lista todos os agendamentos ativos"""
    db = get_db()    

    try:
        query = "SELECT A.*, GP.nome FROM agendamentos A INNER JOIN grupo_mensagens GP on A.grupo_id = GP.id"
        result = db.execute_query(query)
        return result
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()

def excluir_agendamento(agendamento_id):
    """Remove um agendamento"""
    db = get_db()

    try:
        query = "DELETE FROM agendamentos WHERE id = %s"
        db.execute_query(query, (agendamento_id,))
        return {"message": "Agendamento removido com sucesso"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()
