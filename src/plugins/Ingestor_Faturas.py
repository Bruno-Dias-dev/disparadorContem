import psycopg2
import pandas as pd

# Configurar logs
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Conectar ao banco de dados
try:
    conn = psycopg2.connect(
        database="BD_Dom",
        user="postgres",
        password="Cudebila@123",
        host="localhost",
        port=5432
    )
    cursor = conn.cursor()
    logging.info("Conectado ao banco de dados!")
except Exception as e:
    logging.error("Erro ao conectar ao banco de dados: %s", e)
    exit()

# Ler a planilha
file_path = "downloads/Fatura_HM3577MPD55A241220123106.xlsx"
try:
    df = pd.read_excel(file_path)
    logging.info("Planilha carregada com sucesso!")
    logging.info("Cabeçalho da planilha: %s", df.columns.tolist())
except Exception as e:
    logging.error("Erro ao carregar a planilha: %s", e)
    exit()

# Inserir os dados na tabela clientes
for index, row in df.iterrows():
    try:
        cursor.execute("""
            INSERT INTO clientes (
                nome_titular, cpf_titular, telefone, celular, email, endereco, bairro, municipio, uf, cep, pessoa_juridica
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (cpf_titular) DO UPDATE SET
                telefone = EXCLUDED.telefone,
                celular = EXCLUDED.celular,
                email = EXCLUDED.email,
                endereco = EXCLUDED.endereco,
                bairro = EXCLUDED.bairro,
                municipio = EXCLUDED.municipio,
                uf = EXCLUDED.uf,
                cep = EXCLUDED.cep,
                pessoa_juridica = EXCLUDED.pessoa_juridica;
        """, (
            row['Nome Titular'],
            row['CPF Titular'],
            row['Telefone'],
            row['Celular'],
            row['Email'],
            row['Endereço'],
            row['Bairro'],
            row['Município'],
            row['UF'],
            row['CEP'],
            False
        ))
        logging.info("Inserido ou atualizado: %s", row['Nome Titular'])
    except Exception as e:
        conn.rollback()  # Faz rollback em caso de erro
        logging.error("Erro ao inserir ou atualizar cliente %s: %s", row['Nome Titular'], e)

# Confirmar alterações e fechar conexão
try:
    conn.commit()
    cursor.close()
    conn.close()
    logging.info("Dados inseridos com sucesso!")
except Exception as e:
    logging.error("Erro ao finalizar a conexão: %s", e)
