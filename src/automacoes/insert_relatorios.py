import sys
import os
import re

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import pandas as pd
from psycopg2 import sql
from config.conn import PostgresConnection 

# Configurações do Banco de Dados
DB_CONFIG = {
    "host": "localhost",
    "database": "contem",
    "user": "postgres",
    "password": "051295",
    "port": 5432
}

def normalize_column_name(column_name):
    """Remove caracteres especiais e transforma o nome da coluna em minúsculas."""
    return re.sub(r"\W+", "_", column_name).lower().strip("_")


def import_excel_to_postgres(excel_file, sheet_name, db, table_name):
    db.connect()    

    print("📂 Lendo arquivo Excel...")
    df = pd.read_excel(excel_file, sheet_name=sheet_name, dtype=str)  

    try:
        column_map = {col: normalize_column_name(col) for col in df.columns}
        df.rename(columns=column_map, inplace=True)  # Renomeia as colunas do DataFrame

        # Lista de colunas normalizadas para criação da tabela
        columns = [f'"{col}"' for col in df.columns]

        # Define os tipos de colunas dinamicamente
        column_definitions_list = []
        for col in df.columns:
            col_type = "TEXT"  # Padrão
            if df[col].dtype == "int64":
                col_type = "INTEGER"
            elif df[col].dtype == "float64":
                col_type = "FLOAT"

            column_definitions_list.append(f'"{col}" {col_type}')

        column_definitions = ", ".join(column_definitions_list)

        print(f"🛠 Criando tabela '{table_name}'...")
        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS "{table_name}" ({column_definitions});
        '''

        # Debug: Exibir a query SQL gerada
        print("🔎 Query de criação da tabela:")
        print(create_table_query)

        # Executar a criação da tabela
        db.execute_query(create_table_query)
        print(f"✅ Tabela '{table_name}' criada com sucesso.")

        # Substituir NaN por None antes da inserção
        df = df.where(pd.notna(df), None)

        # Inserir dados na tabela
        for _, row in df.iterrows():
            db.insert_table(
                table=table_name,
                columns=[col.replace("\"", "") for col in columns],  # Remover aspas extras
                values=row.tolist()
            )

        print(f"✅ Dados importados com sucesso para a tabela '{table_name}'.")

    except Exception as e:
        print(f"❌ Erro ao importar dados: {e}")

    finally:
        db.close()


def main():
    print("🔗 Conectando ao banco de dados...")
    db = PostgresConnection(**DB_CONFIG)

    # Caminho absoluto do arquivo Excel
    # excel_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../docs/contratos.xlsx"))
    excel_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../docs/faturas.xlsx"))
    print("📂 Caminho do arquivo Excel:", excel_file)

    print("📥 Importando dados do Excel para o PostgreSQL...")
    import_excel_to_postgres(excel_file, "Planilha", db, "relatorio_faturas")

if __name__ == "__main__":
    main()
