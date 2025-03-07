from config.conn import PostgresConnection
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Configuração do banco de dados
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


def list_tb(table: str = "faturas",page: int = 1, page_size: int = 100):
    db = get_db()    
    try:
        offset = (page - 1) * page_size
        query = f'SELECT * FROM {table} LIMIT {page_size} OFFSET {offset}'
        result = db.execute_query(query)
        return result
    except Exception as e:
        print(f"❌ Erro ao capturar dados: {e}")
        return {"error": str(e)}
    finally:
        db.close()        
        
def list_tb_contratos(page: int = 1, page_size: int = 100):
    db = get_db()
    
    try:
        offset = (page - 1) * page_size
        query = f'SELECT * FROM relatorio_contratos ORDER BY "id_contrato" LIMIT {page_size} OFFSET {offset}'
        result = db.execute_query(query)
        return result
    except Exception as e:
        print(f"❌ Erro ao capturar dados: {e}")
        return {"error": str(e)}
    finally:
        db.close()

def list_tb_faturas():
    db = get_db()
    
    try:
        query = 'SELECT * FROM relatorio_faturas ORDER BY "id_fatura"'
        result = db.execute_query(query)
        return result  # Retorna a lista de convênios
    except Exception as e:
        print(f"❌ Erro ao capturar dados: {e}")
        return {"error": str(e)}
    finally:
        db.close()

def list_convenios():
    """Busca os convênios da tabela relatorio_contratos no banco de dados."""
    db = get_db()
    
    try:
        query = 'SELECT DISTINCT "convênio" FROM relatorio_contratos ORDER BY "convênio"'
        result = db.execute_query(query)
        return result  # Retorna a lista de convênios
    except Exception as e:
        print(f"❌ Erro ao capturar dados: {e}")
        return {"error": str(e)}
    finally:
        db.close()

def list_estipulantes():
    """Busca os estipulantes da tabela relatorio_contratos no banco de dados."""
    db = get_db()
    
    try:
        query = 'SELECT DISTINCT "estipulante" FROM relatorio_contratos ORDER BY "estipulante"'
        result = db.execute_query(query)
        return result  
    except Exception as e:
        print(f"❌ Erro ao capturar dados: {e}")
        return {"error": str(e)}
    finally:
        db.close()

def list_status_contrato():
    """Busca os status_do_contrato da tabela relatorio_contratos no banco de dados."""
    db = get_db()
    
    try:
        query = 'SELECT DISTINCT "status_do_contrato" FROM relatorio_contratos ORDER BY "status_do_contrato"'
        result = db.execute_query(query)
        return result  
    except Exception as e:
        print(f"❌ Erro ao capturar dados: {e}")
        return {"error": str(e)}
    finally:
        db.close()

def list_alerta_contrato():
    """Busca os Alerta da tabela relatorio_contratos no banco de dados."""
    db = get_db()
    
    try:
        query = 'SELECT DISTINCT "alerta" FROM relatorio_contratos WHERE alerta IS NOT NULL  ORDER BY "alerta"'
        result = db.execute_query(query)
        return result  
    except Exception as e:
        print(f"❌ Erro ao capturar dados: {e}")
        return {"error": str(e)}
    finally:
        db.close()

def create_grupo_mensagens(nome, convenios, estipulantes, status_contratos, alertas_contratos, ativo, pdf):
    """Cria um novo grupo de mensagens no banco de dados."""
    db = get_db()

    try:
        table = "grupo_mensagens"
        columns = ["nome", "convenios", "estipulantes", "status_contratos", "alertas_contratos", "ativo", "pdf"]
        values = [
            nome,
            json.dumps(convenios) if convenios else None,  # Converte para JSON
            json.dumps(estipulantes) if estipulantes else None,
            json.dumps(status_contratos) if status_contratos else None,
            json.dumps(alertas_contratos) if alertas_contratos else None,
            ativo,
            pdf
        ]

        db.insert_table(table=table, columns=columns, values=values)
        return {"message": "Grupo criado com sucesso!"}

    except Exception as e:
        print(f"❌ Erro ao inserir grupo de mensagens: {e}")
        return {"error": str(e)}

    finally:
        db.close()

def get_grupos_mensagens():
    """Retorna todos os grupos de mensagens."""
    db = get_db()

    try:
        query = "SELECT * FROM grupo_mensagens ORDER BY created DESC"
        return db.execute_query(query)

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()

def get_grupo_by_id(grupo_id):
    """Busca um grupo pelo ID."""
    db = get_db()

    try:
        query = "SELECT * FROM grupo_mensagens WHERE id = %s"
        result = db.execute_query(query, (grupo_id,))
        return result[0] if result else None

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()
        
def update_grupo_mensagens(grupo_id, nome, convenios, estipulantes, status_contratos, alertas_contratos):
    """Atualiza um grupo de mensagens."""
    db = get_db()

    try:
        query = """
        UPDATE grupo_mensagens 
        SET nome = %s, convenios = %s, estipulantes = %s, status_contratos = %s, alertas_contratos = %s, modified = CURRENT_TIMESTAMP 
        WHERE id = %s
        """
        values = (
            nome,
            json.dumps(convenios) if convenios else None,  # Converte para JSON
            json.dumps(estipulantes) if estipulantes else None,
            json.dumps(status_contratos) if status_contratos else None,
            json.dumps(alertas_contratos) if alertas_contratos else None,
            grupo_id
        )
        
        db.execute_query(query, values)
        return {"message": "Grupo atualizado com sucesso!"}

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()
        
def delete_grupo_mensagens(grupo_id):
    """Remove um grupo de mensagens."""
    db = get_db()

    try:
        query = "DELETE FROM grupo_mensagens WHERE id = %s"
        db.execute_query(query, (grupo_id,))
        return {"message": "Grupo removido com sucesso!"}

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()        