import pandas as pd
import logging
import psycopg2
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Caminho para o arquivo
file_path = "C:/Users/amirc/Downloads/Inadimplencia_67RYYL4SR54G241231144737.xlsx"

# Verificar se o arquivo existe
if not os.path.exists(file_path):
    logging.error("Arquivo não encontrado: %s", file_path)
    exit()

# Ler a planilha
try:
    df = pd.read_excel(file_path)
    logging.info("Planilha carregada com sucesso!")
except Exception as e:
    logging.error("Erro ao carregar a planilha: %s", e)
    exit()

# Substituir valores vazios por None
df = df.where(pd.notnull(df), None)

# Conectar ao banco de dados
try:
    conn = psycopg2.connect(
        database="BD_DOM",
        user="postgres",
        password="pharos",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    logging.info("Conectado ao banco de dados!")
except Exception as e:
    logging.error("Erro ao conectar ao banco de dados: %s", e)
    exit()


# Inserir os dados na tabela relatorio_inadimplencia
for index, row in df.head(10).iterrows():
    try:
        if pd.isna(row['Código Contrato']):
            logging.error("Erro: 'Código Contrato' está ausente na linha %d", index)
            continue
        
        # Inserir na tabela relatorio_inadimplencia
        cursor.execute("""
            INSERT INTO relatorio_inadimplencia (
                id_relatorio_inadimplencia, contrato_id, codigo_contrato_id, numero_proposta, nome_titular, data_spc, created, modified
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id_relatorio_inadimplencia) DO UPDATE SET
                contrato_id = EXCLUDED.contrato_id,
                codigo_contrato_id = EXCLUDED.codigo_contrato_id,
                numero_proposta = EXCLUDED.numero_proposta,
                nome_titular = EXCLUDED.nome_titular,
                data_spc = EXCLUDED.data_spc,
                modified = EXCLUDED.modified
        """, (
            row['ID Contrato'], row['Código Contrato'], row['Número da Proposta'], row['Titular'], row['Data Spc']
        ))

        # Inserir na tabela grupo_produtor
        cursor.execute(""" 
            INSERT INTO grupo_produtor (  
                       id_grupo_produtor, nome, created, modified
            ) VALUES (%s, %s, %s, %s)
                       ON CONFLICT (id_grupo_produtor) DO UPDATE SET
                nome = EXCLUDED.nome,
                modified = EXCLUDED.modified""",
                (row['Grupo Produtor'] 
                ))

        # Inserir na tabela plano
        cursor.execute("""
                       INSERT INTO plano (
                            matricula, created, modified
                       ) VALUES (%s, %s, %s)""",
                          (row['Marca Óptica Titular']
                          ))
        
        # Inserir na tabela superior    
        cursor.execute("""
                       INSERT INTO superior (
                       nome, created, modified
                       ) VALUES (%s, %s, %s)""",
                          (row['Produtor']
                          ))
        
        # Inserir na tabela cliente
        cursor.execute("""
                       INSERT INTO cliente (
                       nome, matricula, cpf_titular, endereco, status, created, modified
                       ) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                          (row['Titular'], row['Marca Óptica Titular'], row['CPF Titular'], row['Endereço'], row['Status do Contrato']
                          ))
        
        # Inserir na tabela operadora
        cursor.execute("""
                       INSERT INTO operadora (
                       nome, cnpj, pessoa_juridica , telefone_atendimento, celular_atendimento, email_atendimento, status, created, modified
                       ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                          (row['Operadora'], row['CNPJ'], row['Pessoa Jurídica'], row['Telefone Atendimento'], row['Celular Atendimento'], row['Email Atendimento'], row['Status do Contrato']
                          ))
        # Inserir na tabela faturas
        cursor.execute("""
                       INSERT INTO faturas (
                       id_faturas, dia_vencimento, valor, status, data_saldo, alerta, data_cancelamento, motivo_cancelamento, created, modified
                       ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                          (row['ID Faturas'], row['Dia de Vencimento'],row['Saldo Devedor'], row['Status do Contrato'], row['Data do Saldo'], row['Alerta'], row['Data de Cancelamento'], row['Motivo de Cancelamento']
                          ))

        conn.commit()
    except Exception as e:
        logging.error("Erro ao inserir ou atualizar contrato %s: %s", row['Código Contrato'], e)

cursor.close()
conn.close()