import pandas as pd
import psycopg2
import logging
from datetime import datetime

# Configuração de logging
logging.basicConfig(level=logging.INFO)

# Carregar a planilha
file_path = "C:/Users/amirc/OneDrive - PHAROS GESTAO/Grupo Contém/9 - BI/Robozinho/Airflow/Airflow/docs/Inadimplencia_75KGLKMEXV3E241227121723.xlsx"
df = pd.read_excel(file_path)

# Substituir valores vazios por None para evitar problemas no banco
df = df.where(pd.notnull(df), None)

# Conexão com o banco de dados
try:
    conn = psycopg2.connect(
        database="BD_Dom",
        user="postgres",
        password="pharos",
        host="localhost",
        port=5432
    )
    cursor = conn.cursor()
    logging.info("Conectado ao banco de dados!")
except Exception as e:
    logging.error("Erro ao conectar ao banco de dados: %s", e)
    exit()

# Função para tratar datas e valores ausentes
def safe_date(value):
    return value if pd.notna(value) else None

def safe_str(value):
    return value if value else None

# Inserção dos dados
for index, row in df.head(10).iterrows():
    try:
        contrato_id = row.get('ID Contrato')
        codigo_contrato = row.get('Código Contrato')
        numero_proposta = row.get('Número da Proposta')
        titular = row.get('Titular')
        data_spc = safe_date(row.get('Data Spc'))
        grupo_produtor = row.get('Grupo Produtor')
        cpf_titular = row.get('CPF Titular')
        endereco = row.get('Endereço')
        status = row.get('Status do Contrato')
        marca_optica = row.get('Marca Óptica Titular')
        operadora = row.get('Operadora')

        # Inserção na tabela relatorio_inadimplencia
        cursor.execute("""
            INSERT INTO relatorio_inadimplencia (
                contrato_id, codigo_contrato, numero_proposta, nome_titular, data_spc, created, modified
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (contrato_id) DO UPDATE SET
                codigo_contrato = EXCLUDED.codigo_contrato,
                numero_proposta = EXCLUDED.numero_proposta,
                nome_titular = EXCLUDED.nome_titular,
                data_spc = EXCLUDED.data_spc,
                modified = EXCLUDED.modified
        """, (
            contrato_id, codigo_contrato, numero_proposta, titular, data_spc, datetime.now(), datetime.now()
        ))

        # Inserção na tabela grupo_produtor
        if grupo_produtor:
            cursor.execute("""
                INSERT INTO grupo_produtor (
                    id_grupo_produtor, nome, created, modified
                ) VALUES (%s, %s, %s, %s)
                ON CONFLICT (id_grupo_produtor) DO UPDATE SET
                    nome = EXCLUDED.nome,
                    modified = EXCLUDED.modified
            """, (
                grupo_produtor, grupo_produtor, datetime.now(), datetime.now()
            ))

        # Inserção na tabela cliente
        cursor.execute("""
            INSERT INTO cliente (
                nome, matricula, cpf_titular, endereco, status, created, modified
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (matricula) DO UPDATE SET
                nome = EXCLUDED.nome,
                cpf_titular = EXCLUDED.cpf_titular,
                endereco = EXCLUDED.endereco,
                status = EXCLUDED.status,
                modified = EXCLUDED.modified
        """, (
            titular, marca_optica, cpf_titular, endereco, status, datetime.now(), datetime.now()
        ))

        # Inserção na tabela plano
        if marca_optica:
            cursor.execute("""
                INSERT INTO plano (
                    matricula, created, modified
                ) VALUES (%s, %s, %s)
                ON CONFLICT (matricula) DO NOTHING
            """, (
                marca_optica, datetime.now(), datetime.now()
            ))

        # Inserção na tabela superior
        produtor = row.get('Produtor')
        if produtor:
            cursor.execute("""
                INSERT INTO superior (
                    nome, created, modified
                ) VALUES (%s, %s, %s)
                ON CONFLICT (nome) DO NOTHING
            """, (
                produtor, datetime.now(), datetime.now()
            ))

        # Inserção na tabela operadora
        cnpj = row.get('CNPJ')
        pessoa_juridica = row.get('Pessoa Jurídica')
        telefone_atendimento = row.get('Telefone Atendimento')
        celular_atendimento = row.get('Celular Atendimento')
        email_atendimento = row.get('Email Atendimento')

        if operadora:
            cursor.execute("""
                INSERT INTO operadora (
                    nome, cnpj, pessoa_juridica, telefone_atendimento, celular_atendimento, email_atendimento, status, created, modified
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (cnpj) DO NOTHING
            """, (
                operadora, cnpj, pessoa_juridica, telefone_atendimento, celular_atendimento, email_atendimento, status, datetime.now(), datetime.now()
            ))

        # Inserção na tabela faturas
        dia_vencimento = row.get('Dia de Vencimento')
        saldo_devedor = row.get('Saldo Devedor')
        data_saldo = safe_date(row.get('Data do Saldo'))
        alerta = row.get('Alerta')
        data_cancelamento = safe_date(row.get('Data de Cancelamento'))
        motivo_cancelamento = row.get('Motivo de Cancelamento')

        cursor.execute("""
            INSERT INTO faturas (
                id_faturas, dia_vencimento, valor, status, data_saldo, alerta, data_cancelamento, motivo_cancelamento, created, modified
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id_faturas) DO NOTHING
        """, (
            contrato_id, dia_vencimento, saldo_devedor, status, data_saldo, alerta, data_cancelamento, motivo_cancelamento, datetime.now(), datetime.now()
        ))

        conn.commit()
    except Exception as e:
        logging.error("Erro ao inserir dados do contrato %s: %s", codigo_contrato, e)
        conn.rollback()

# Fechar a conexão
cursor.close()
conn.close()

logging.info("Processo de inserção concluído!")
