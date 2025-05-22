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
        return {"error": str(e)}
    finally:
        db.close()

def list_convenios():
    """Busca os convênios da tabela relatorio_contratos no banco de dados."""
    db = get_db()
    
    try:
        query = 'SELECT DISTINCT "convenio" FROM relatorio_contratos ORDER BY "convenio"'
        result = db.execute_query(query)
        return result  # Retorna a lista de convênios
    except Exception as e:
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
        return {"error": str(e)}
    finally:
        db.close()

def list_alerta_contrato():
    """Busca os Alerta da tabela relatorio_contratos no banco de dados."""
    db = get_db()
    
    try:
        query = 'SELECT DISTINCT "alerta" FROM relatorio_contratos ORDER BY "alerta"'
        result = db.execute_query(query)
        return result  
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()

def create_grupo_mensagens(nome, convenios, estipulantes, status_contratos, alertas_contratos, ativo, pdf, fase):
    """Cria um novo grupo de mensagens no banco de dados."""
    db = get_db()

    try:
        table = "grupo_mensagens"
        columns = ["nome", "convenios", "estipulantes", "status_contratos", "alertas_contratos", "ativo", "pdf", "fase"]
        values = [
            nome,
            json.dumps(convenios) if convenios else None,  # Converte para JSON
            json.dumps(estipulantes) if estipulantes else None,
            json.dumps(status_contratos) if status_contratos else None,
            json.dumps(alertas_contratos) if alertas_contratos else None,
            ativo,
            pdf,
            fase
        ]

        db.insert_table(table=table, columns=columns, values=values)
        return {"message": "Grupo criado com sucesso!"}

    except Exception as e:
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
        
def update_grupo_mensagens(grupo_id, nome, convenios, estipulantes, status_contratos, alertas_contratos,ativo, pdf):
    """Atualiza um grupo de mensagens."""
    db = get_db()

    try:
        query = """
        UPDATE grupo_mensagens 
        SET nome = %s, convenios = %s, estipulantes = %s, status_contratos = %s, alertas_contratos = %s, ativo = %s, pdf= %s, modified = CURRENT_TIMESTAMP 
        WHERE id = %s
        """
        values = (
            nome,
            json.dumps(convenios) if convenios else None,  # Converte para JSON
            json.dumps(estipulantes) if estipulantes else None,
            json.dumps(status_contratos) if status_contratos else None,
            json.dumps(alertas_contratos) if alertas_contratos else None,
            ativo,
            pdf,
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
        
def get_faturas_por_grupo(grupo_id: int):
    """Seleciona todas as faturas associadas a um grupo_id, lidando com NULL em todas as colunas"""
    db = get_db()
    
    try:
        query = """
    SELECT 
        rf.codigo_da_fatura,
        celular,
        qtde_dias_atraso
    FROM 
        relatorio_faturas rf
    JOIN grupo_mensagens gm 
        ON (
            gm.convenios IS NULL 
            OR gm.convenios->'valores' @> '["Todos"]'::jsonb
            OR rf.convenio_do_fatura = ANY (
                SELECT jsonb_array_elements_text(gm.convenios->'valores')
            )
        )
        AND (
            gm.estipulantes IS NULL 
            OR rf.estipulante = ANY (
                SELECT jsonb_array_elements_text(gm.estipulantes->'valores')
            )
        )
        AND (
            gm.status_contratos IS NULL 
            OR rf.status_do_contrato = ANY (
                SELECT jsonb_array_elements_text(gm.status_contratos->'valores')
            )
        )
        AND (
            gm.alertas_contratos IS NULL 
            OR jsonb_array_length(gm.alertas_contratos->'valores') = 0 
            OR rf.alerta = ANY (
                SELECT jsonb_array_elements_text(gm.alertas_contratos->'valores')
            )
        )
        AND (
            gm.fase IS NULL
            OR gm.fase = '0'
            OR (
                qtde_dias_atraso::INTEGER BETWEEN 
                SPLIT_PART(gm.fase, '-', 1)::int AND 
                SPLIT_PART(gm.fase, '-', 2)::int
            )
        )
    WHERE 
        gm.id = %s
        AND
        DATE(rf.updated_at) = CURRENT_DATE;
    """
        result = db.execute_query(query, (grupo_id,))    
        return result

    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()

def list_mensagens():
    """Lista todas as mensagens."""
    db = get_db()

    try:
        query = "SELECT * FROM mensagens ORDER BY id DESC"
        result = db.execute_query(query)
        return result

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()        

def create_mensagem(mensagem, ativo, titulo):
    """Cria uma nova mensagem."""
    db = get_db()

    try:
        table = "mensagens"
        columns = ["mensagem", "ativo", "title"]
        values = [mensagem, ativo, titulo]

        db.insert_table(table=table, columns=columns, values=values)
        return {"message": "Mensagem criada com sucesso!"}

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()

def get_msg_by_id(mensagem_id):
    """Busca a mensagem pelo ID."""
    db = get_db()

    try:
        query = "SELECT * FROM mensagens WHERE id = %s"
        result = db.execute_query(query, (mensagem_id,))
        return result[0] if result else None

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()
        
def update_mensagens(id, mensagem, ativo, titulo):
    """Atualiza uma mensagem."""
    db = get_db()

    try:
        query = """
        UPDATE mensagens 
        SET mensagem = %s, ativo = %s, title = %s, modified = CURRENT_TIMESTAMP 
        WHERE id = %s
        """
        values = (mensagem, ativo, titulo, id)

        db.execute_query(query, values)
        return {"message": "Mensagem atualizada com sucesso!"}

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()

def delete_mensagem(mensagem_id):
    """Remove uma mensagem."""
    db = get_db()

    try:
        query = "DELETE FROM mensagens WHERE id = %s"
        db.execute_query(query, (mensagem_id,))
        return {"message": "Mensagem removida com sucesso!"}

    except Exception as e:
        return {"error": str(e)}

    finally:
        db.close()