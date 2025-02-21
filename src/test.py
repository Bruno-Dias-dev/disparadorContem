import psycopg2
import os
from psycopg2 import OperationalError
from dotenv import load_dotenv

load_dotenv()
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
DATABASE = os.getenv("DB_NAME")

def test_postgres_connection():
    try:
        connection = psycopg2.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,  # localhost ou IP interno
            port=PORT,  # porta padrão
            database=DATABASE
        )
        print("✅ Conexão com o PostgreSQL bem-sucedida!")
        connection.close()
    except OperationalError as e:
        print(f"🚫 Erro ao conectar ao PostgreSQL: {e}")

test_postgres_connection()