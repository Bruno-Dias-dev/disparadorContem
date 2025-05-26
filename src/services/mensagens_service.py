from config.conn import PostgresConnection
import os
import json
from dotenv import load_dotenv
from fastapi import HTTPException, status
from typing import List, Dict, Any
import pandas as pd
import io

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
        
def insert_faturas_batch(faturas_data: List[Dict[str, Any]]):
    db = get_db()
    inserted_count = 0
    try:
        table = "upload_faturas"
        columns = ["codigo_da_fatura", "celular", "nome", "grupo_id"]

        for fatura in faturas_data:
            values = [
                fatura["codigo_da_fatura"],
                fatura["celular"],
                fatura["nome"],
                fatura["grupo_id"]
            ]
            db.insert_table(table=table, columns=columns, values=values)
            inserted_count += 1
        return {"message": f"{inserted_count} faturas inseridas com sucesso!"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao inserir faturas no banco de dados: {str(e)}"
        )
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
        raw_id_result = db.execute_query("SELECT id FROM grupo_mensagens WHERE nome = %s ORDER BY created DESC LIMIT 1;", (nome,))
        
        if raw_id_result and isinstance(raw_id_result, (list, tuple)) and len(raw_id_result) > 0:
            if isinstance(raw_id_result[0], dict): 
                grupo_id = raw_id_result[0].get("id")
            elif isinstance(raw_id_result[0], (list, tuple)):
                grupo_id = raw_id_result[0][0]
            else: 
                grupo_id = raw_id_result[0]
        else:
            raise ValueError("ID do grupo não foi retornado ou resultado inválido.")
        
        return {"message": "Grupo criado com sucesso!", "grupo_id": grupo_id}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao criar grupo: {str(e)}")
        # return {"error": str(e)}

    finally:
        db.close()

def get_grupos_mensagens():
    """Retorna todos os grupos de mensagens."""
    db = get_db()

    try:
        query = "SELECT * FROM grupo_mensagens WHERE ativo = 't' ORDER BY created DESC"
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
    """
    Seleciona faturas associadas a um grupo_id.
    Prioriza 'upload_faturas', se vazio, busca em 'relatorio_faturas' com filtros do grupo.
    """
    db = get_db()
    
    try:
        # --- 1. Tentar buscar em upload_faturas ---
        upload_faturas_query = """
        SELECT
            uf.codigo_da_fatura,
            uf.celular,
            NULL AS qtde_dias_atraso -- Adicionado para consistência de colunas com relatorio_faturas
        FROM
            upload_faturas uf
        WHERE
            uf.grupo_id = %s
            AND uf.enviado = FALSE; -- Supondo que você só quer faturas não enviadas/processadas
        """
        
        faturas_encontradas = db.execute_query(upload_faturas_query, (grupo_id,))
        
        if faturas_encontradas:
            return faturas_encontradas
        
        # --- 2. Se não houver faturas em upload_faturas, buscar em relatorio_faturas ---
        # Primeiro, obtenha os detalhes do grupo para aplicar os filtros.
        grupo_detalhes_query = """
        SELECT
            nome, convenios, estipulantes, status_contratos, alertas_contratos, fase
        FROM
            grupo_mensagens
        WHERE
            id = %s;
        """
        grupo_detalhes_raw = db.execute_query(grupo_detalhes_query, (grupo_id,))
        
        if not grupo_detalhes_raw:
            # Se o grupo não for encontrado, retorna uma lista vazia
            return [] 
        
        # Assume que db.execute_query para SELECT retorna uma lista de dicionários
        grupo = grupo_detalhes_raw[0] 
        
        # --- CORREÇÃO AQUI: NÃO USAR json.loads() ---
        # Se 'db.execute_query' já retorna 'jsonb' como dicionários Python,
        # basta usá-los diretamente. Adicionei um fallback robusto.
        
        convenios = grupo.get('convenios')
        if not isinstance(convenios, dict) or convenios is None:
            convenios = {"valores": []} # Fallback se não for um dicionário válido ou for None

        estipulantes = grupo.get('estipulantes')
        if not isinstance(estipulantes, dict) or estipulantes is None:
            estipulantes = {"valores": []}

        status_contratos = grupo.get('status_contratos')
        if not isinstance(status_contratos, dict) or status_contratos is None:
            status_contratos = {"valores": []}

        alertas_contratos = grupo.get('alertas_contratos')
        if not isinstance(alertas_contratos, dict) or alertas_contratos is None:
            alertas_contratos = {"valores": []}
            
        # A fase já é string ou None, não precisa de tratamento especial
        fase = grupo.get('fase') 

        # Constrói a query dinâmica para relatorio_faturas
        relatorio_faturas_select = """
        SELECT
            rf.codigo_da_fatura,
            rf.celular,
            rf.qtde_dias_atraso
        FROM
            relatorio_faturas rf
        """
        
        conditions = []
        query_params = []
        
        # Adiciona condições baseadas nos filtros do grupo
        if convenios and convenios.get('valores') and "Todos" not in convenios['valores']:
            conditions.append("rf.convenio_do_fatura = ANY (%s::text[])")
            query_params.append(convenios['valores'])
        
        if estipulantes and estipulantes.get('valores'):
            conditions.append("rf.estipulante = ANY (%s::text[])")
            query_params.append(estipulantes['valores'])

        if status_contratos and status_contratos.get('valores'):
            conditions.append("rf.status_do_contrato = ANY (%s::text[])")
            query_params.append(status_contratos['valores'])
            
        if alertas_contratos and alertas_contratos.get('valores'):
            conditions.append("rf.alerta = ANY (%s::text[])")
            query_params.append(alertas_contratos['valores'])
        
        # Lógica para Fase (qtde_dias_atraso)
        if fase and fase != '0': 
            try:
                min_dias, max_dias = map(int, fase.split('-'))
                conditions.append("rf.qtde_dias_atraso::INTEGER BETWEEN %s AND %s")
                query_params.extend([min_dias, max_dias])
            except ValueError:
                print(f"Aviso: Fase '{fase}' não está no formato esperado (min-max). Ignorando filtro de fase.")
                pass
            
        conditions.append("DATE(rf.updated_at) = CURRENT_DATE") 

        # Constrói a query final
        final_query = f"{relatorio_faturas_select}"
        if conditions:
            final_query += " WHERE " + " AND ".join(conditions)
        
        result = db.execute_query(final_query, tuple(query_params))
        
        return result

    except Exception as e:
        print(f"Erro em get_faturas_por_grupo: {e}")
        # Lança HTTPException para que o FastAPI capture e retorne um erro 500
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao buscar faturas: {str(e)}")
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