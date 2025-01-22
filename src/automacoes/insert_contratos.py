import pandas as pd
import psycopg2

# Configurações do Banco de Dados
DB_CONFIG = {
    "host": "localhost",
    "database": "contem",
    "user": "postgres",
    "password": "C@med2024",
    "port": 5432
}

def carregar_excel_dados(caminho_dados):
    """Carrega o arquivo Excel com os registros."""
    return pd.read_excel(caminho_dados)

def carregar_mapeamento(caminho_mapeamento):
    """Carrega o arquivo Excel com o mapeamento (cabeçalho → coluna → tabela)."""
    return pd.read_excel(caminho_mapeamento)

def processar_mapeamento(mapeamento_df):
    """Transforma o mapeamento em uma estrutura de dicionário para consulta rápida."""
    mapeamento = {}
    for _, row in mapeamento_df.iterrows():
        coluna_excel = row['Campo do Cabeçalho da Planilha Originária']
        tabela = row['Tabela no Banco de Dados']
        coluna_banco = row['Coluna no Banco de Dados']
        
        if tabela not in mapeamento:
            mapeamento[tabela] = {}
        mapeamento[tabela][coluna_excel] = coluna_banco
    return mapeamento

def inserir_no_banco(conexao, tabela, colunas, valores):
    """Insere os valores na tabela especificada."""
    try:
        with conexao.cursor() as cursor:
            colunas_str = ', '.join(colunas)
            placeholders = ', '.join(['%s'] * len(valores))
            query = f"INSERT INTO {tabela} ({colunas_str}) VALUES ({placeholders})"
            cursor.execute(query, valores)
        conexao.commit()
        print(f"Dados inseridos com sucesso na tabela {tabela}.")
    except Exception as e:
        conexao.rollback()
        print(f"Erro ao inserir dados na tabela {tabela}: {e}")

def main():
    # Caminhos para os arquivos Excel
    caminho_dados = "C:/Users/HozanaISF/Documents/Desenvolvimento/Python/Airflow/docs/contratos.xlsx"
    caminho_mapeamento = "C:/Users/HozanaISF/Documents/Desenvolvimento/Python/Airflow/docs/Mapeamento_Campos_Banco_Dados.xlsx"

    # Carregar os dados e o mapeamento
    dados_df = carregar_excel_dados(caminho_dados).head(5)
    mapeamento_df = carregar_mapeamento(caminho_mapeamento)

    # Processar o mapeamento
    mapeamento = processar_mapeamento(mapeamento_df)

    # Conectar ao banco de dados
    conexao = psycopg2.connect(**DB_CONFIG)

    # Inserir os dados no banco de acordo com o mapeamento
    for _, row in dados_df.iterrows():
        tabelas_insercao = {}

        # Organizar os dados por tabela
        for tabela, colunas in mapeamento.items():
            colunas_banco = []
            valores = []
            for coluna_excel, coluna_banco in colunas.items():
                if coluna_excel in row and not pd.isna(row[coluna_excel]):
                    colunas_banco.append(coluna_banco)
                    valores.append(row[coluna_excel])

            if colunas_banco:
                if tabela not in tabelas_insercao:
                    tabelas_insercao[tabela] = []
                tabelas_insercao[tabela].append((colunas_banco, valores))

        # Inserir os dados no banco
        for tabela, registros in tabelas_insercao.items():
            for colunas_banco, valores in registros:
                inserir_no_banco(conexao, tabela, colunas_banco, valores)

    # Fechar a conexão
    conexao.close()

if __name__ == "__main__":
    main()
