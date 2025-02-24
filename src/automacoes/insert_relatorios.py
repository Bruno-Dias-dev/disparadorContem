"""
Script para importar dados de um arquivo Excel para uma tabela do PostgreSQL.
Para executar este script, é necessário instalar as bibliotecas pandas e psycopg2.
 - Na função main(), altere o valor da variável excel_file para o caminho absoluto do arquivo Excel.
 - Na função import_excel_to_postgres(), altere o valor da variável table_name para o nome da tabela no banco de dados.
   --- O padrão é "relatorio_NomeFuncionalidade", exemplo: "relatorio_contratos", ou "relatorio_faturas". 
   --- Para cada tabela, é necessário definir um id_column diferente, que será a chave primária da tabela, linha 54.
       Exemplo: id_column = "id_contrato" ou id_column = "id_fatura". Se precisar de mais tabelas, adicione mais elifs e id_columns. 
"""

import sys
import os
import re
import unicodedata
import argparse


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
    # "password": "C@med2024",
    "password": "051295",
    "port": 5432
}

def normalize_column_name(column_name: str) -> str:
    # Remove acentuação
    column_name = unicodedata.normalize("NFKD", column_name).encode("ASCII", "ignore").decode("utf-8")
    
    # Substitui caracteres não alfanuméricos por _
    column_name = re.sub(r"\W+", "_", column_name).lower().strip("_")
    
    return column_name

def create_table(table_name, column_definitions, db, id_column="id"):
    print(f"🛠 Criando tabela '{table_name}'...")
    create_table_query = f'''
        CREATE TABLE IF NOT EXISTS "{table_name}" ({column_definitions}, PRIMARY KEY ("{id_column}"));
        '''
    # Debug: Exibir a query SQL gerada
    print("🔎 Query de criação da tabela:")
    print(create_table_query)

    # Executar a criação da tabela
    db.execute_query(create_table_query)
    print(f"✅ Tabela '{table_name}' criada com sucesso.")

def import_excel_to_postgres(excel_file, sheet_name, db, table_name, id_column="id"):
    db.connect()    

    print("📂 Lendo arquivo Excel...")
    df = pd.read_excel(excel_file, sheet_name=sheet_name, dtype=str)  

    try:
        if table_name == "relatorio_faturas":
            id_column = "id_fatura"
        elif table_name == "relatorio_contratos":
            id_column = "id_contrato"
        elif table_name == "relatorio_inadimplencia":
            id_column = "id_contrato"
        else:
            id_column = "id"

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

        create_table(table_name, column_definitions, db, id_column)

        # Substituir NaN por None antes da inserção
        df = df.where(pd.notna(df), None)

        # Inserir dados na tabela
        for _, row in df.iterrows():
            values = row.tolist()
            column_names = [col.replace('"', '') for col in columns]  # Remover aspas extras
            placeholders = ", ".join(["%s"] * len(values))  # Para o INSERT

            update_clause = ", ".join([f'"{col}" = EXCLUDED."{col}"' for col in column_names if col != id_column])

            upsert_query = f"""
            INSERT INTO "{table_name}" ({", ".join(column_names)})
            VALUES ({placeholders})
            ON CONFLICT ("{id_column}") DO UPDATE 
            SET {update_clause};            """

            db.execute_query(upsert_query, values)

        print(f"✅ Dados inseridos ou atualizados com sucesso na tabela '{table_name}'.")

    except Exception as e:
        print(f"❌ Erro ao importar dados: {e}")

    finally:
        db.close()


def main(local_file, table_name):
    print("🔗 Conectando ao banco de dados...")
    db = PostgresConnection(**DB_CONFIG)

    # Caminho absoluto do arquivo Excel
    # excel_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../docs/contratos.xlsx"))
    # excel_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../docs/faturas.xlsx"))
    # excel_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../docs/inadimplencia.xlsx"))
    excel_file = os.path.abspath(os.path.join(os.path.dirname(__file__), local_file))
    print("📂 Caminho do arquivo Excel:", excel_file)

    print("📥 Importando dados do Excel para o PostgreSQL...")
    # import_excel_to_postgres(excel_file, "Planilha", db, "relatorio_faturas")
    # import_excel_to_postgres(excel_file, "Planilha", db, "relatorio_contratos")
    # import_excel_to_postgres(excel_file, "Planilha", db, "relatorio_inadimplencia")
    import_excel_to_postgres(excel_file, "Planilha", db, table_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Importa relatórios para o banco de dados")
    parser.add_argument("local_file", help="Caminho do arquivo Excel")
    parser.add_argument("table_name", help="Nome da tabela no banco de dados")

    args = parser.parse_args()
    main(args.local_file, args.table_name)
