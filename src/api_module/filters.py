import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from config.conn import PostgresConnection

DB_CONFIG = {
    "host": "localhost",
    "database": "contem",
    "user": "postgres",
    "password": "C@med2024",
    # "password": "051295",
    "port": 5432
}


def list_contratos(db):
    try:
        query = 'select distinct "convênio" from relatorio_contratos order by "convênio"'
        result = db.execute_query(query)
        print("🔎 Listando convênios...")
        # for row in db.fetchall():
        return result

    except Exception as e:
        print(f"❌ Erro ao capturar dados: {e}")

    finally:
        db.close()


def main():
    print("🔗 Conectando ao banco de dados...")
    db = PostgresConnection(**DB_CONFIG)
    db.connect()

    list_contratos(db)

if __name__ == "__main__":
    main()
