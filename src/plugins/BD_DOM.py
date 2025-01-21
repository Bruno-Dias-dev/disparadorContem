import psycopg2
import os
from psycopg2 import sql

def criar_banco_dados():
    try:
        # Conexão inicial com o banco de dados padrão (postgres)
        conexao = psycopg2.connect(
            database="postgres",  # Conecte-se ao banco padrão
            user="postgres",
            password="pharos",
            host="localhost",
            port=5432
        )
        conexao.autocommit = True  # Necessário para criar o banco de dados
        cursor = conexao.cursor()

        # Nome do banco de dados a ser criado
        nome_banco = "BD_Dom"

        # Comando SQL para criar o banco de dados com configurações regionais
        cursor.execute(sql.SQL(
            """
            CREATE DATABASE {nome_banco}
            WITH 
                OWNER = postgres
                ENCODING = 'UTF8'
                LC_COLLATE = 'Portuguese_Brazil.1252'
                LC_CTYPE = 'Portuguese_Brazil.1252'
                TABLESPACE = pg_default
                CONNECTION LIMIT = -1;
            """
        ).format(nome_banco=sql.Identifier(nome_banco)))

        print(f"Banco de dados '{nome_banco}' criado com sucesso.")

        # Fecha a conexão inicial
        cursor.close()
        conexao.close()

        # Conecta ao banco recém-criado para confirmar a criação
        nova_conexao = psycopg2.connect(
            database=nome_banco,
            user="postgres",
            password="pharos",
            host="localhost",
            port=5432
        )
        print(f"Conectado ao banco de dados '{nome_banco}' com sucesso.")
        nova_conexao.close()

    except (Exception, psycopg2.DatabaseError) as erro:
        print(f"Erro ao criar o banco de dados: {erro}")
    finally:
        if 'conexao' in locals() and conexao:
            conexao.close()
            print("Conexão inicial encerrada.")

if __name__ == "__main__":
    criar_banco_dados()

# Caminho do arquivo SQL
sql_file_path = "C:/Users/amirc/OneDrive - PHAROS GESTAO/Grupo Contém/9 - BI/Robozinho/PostgresSQL/SCRPT1.sql"

# Verificar se o arquivo existe
if not os.path.exists(sql_file_path):
    raise FileNotFoundError(f"Arquivo SQL não encontrado: {sql_file_path}")

# Conectar ao banco de dados PostgreSQL
conn = psycopg2.connect(
    dbname="BD_Dom",
    user="postgres",
    password="pharos",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Caminho do arquivo SQL
sql_file_path = "C:/Users/amirc/OneDrive - PHAROS GESTAO/Grupo Contém/9 - BI/Robozinho/PostgresSQL/SCRPT1.sql"

# Verificar se o arquivo existe
if not os.path.exists(sql_file_path):
    raise FileNotFoundError(f"Arquivo SQL não encontrado: {sql_file_path}")

# Conectar ao banco de dados PostgreSQL
conn = psycopg2.connect(
    dbname="BD_Dom",
    user="postgres",
    password="pharos",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Ler e executar o script SQL
with open(sql_file_path, 'r') as file:
    sql_script = file.read()

try:
    cur.execute(sql_script)
    conn.commit()
except psycopg2.errors.UndefinedTable as e:
    conn.rollback()
    raise RuntimeError(f"Erro ao executar o script SQL: {e}")
finally:
    cur.close()
    conn.close()