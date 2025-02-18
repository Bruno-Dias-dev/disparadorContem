from config.conn import PostgresConnection
import os
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

load_dotenv()

FUSO_HORARIO_LOCAL = timezone(timedelta(hours=-3))

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

def criar_agendamento(grupo_id, horario_disparo, ativo=True):
    """Cria um novo agendamento de mensagem"""
    db = PostgresConnection(**DB_CONFIG)
    db.connect()
    
    try:
        now = datetime.now(FUSO_HORARIO_LOCAL)
        if isinstance(horario_disparo, str):
            horario_disparo = datetime.fromisoformat(horario_disparo.replace("Z", "-03:00"))
            
        print(f"DEBUG - now (FUSO LOCAL): {now}")
        print(f"DEBUG - horario_disparo : {horario_disparo}")

        # if horario_disparo < now:
        #     print(f"⚠️ Erro: A data/hora de disparo ({horario_disparo}) não pode estar no passado.")
        #     return {"error": "A data/hora de agendamento deve ser no futuro."}

        query = """
        INSERT INTO agendamentos (grupo_id, horario_disparo, ativo)
        VALUES (%s, %s, %s)
        RETURNING id;
        """
        result = db.execute_query(query, (grupo_id, horario_disparo, ativo))

        # Verifica se o resultado é válido
        if result and isinstance(result, list) and len(result) > 0 and "id" in result[0]:
            return {"id": result[0]["id"], "message": "Agendamento criado com sucesso"}
        else:
            print("⚠️ Nenhum ID retornado pela query!")
            return {"error": "Falha ao obter ID do agendamento inserido"}
        
    except Exception as e:
        print("❌ Erro ao criar agendamento:", e)
        return {"error": str(e)}
    finally:
        db.close()

def listar_agendamentos():
    """Lista todos os agendamentos ativos"""
    db = get_db()    

    try:
        query = "SELECT * FROM agendamentos WHERE ativo = TRUE"
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
