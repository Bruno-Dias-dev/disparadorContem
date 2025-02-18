import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

class PostgresConnection:
    def __init__(self, host, database, user, password, port=5432):
        """
        Inicializa a conexão com o banco de dados PostgreSQL.
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    def connect(self):
        """
        Estabelece a conexão com o banco de dados.
        """
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            print("✅ Conexão estabelecida com sucesso!")
        except psycopg2.Error as e:
            print(f"❌ Erro ao conectar ao banco de dados: {e}")
            raise

    def close(self):
        """
        Fecha a conexão com o banco de dados.
        """
        if self.connection:
            self.connection.close()
            print("✅ Conexão fechada com sucesso!")

    def execute_query(self, query, params=None):
        """
        Executa uma consulta SQL (SELECT, INSERT, UPDATE, DELETE).
        """
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                if "returning" in query.lower():
                    result = cursor.fetchone()  
                    return [result] if result else [] 
                
                if query.strip().lower().startswith("select"):
                    result = cursor.fetchall()
                    return result if result else []
                else:
                    self.connection.commit()
                    return None
                
        except psycopg2.Error as e:
            print(f"Erro ao executar consulta: {e}")
            self.connection.rollback()
            raise

    def execute_many(self, query, data_list):
        """
        Executa uma consulta SQL para múltiplos registros.
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.executemany(query, data_list)
                self.connection.commit()
        except psycopg2.Error as e:
            print(f"Erro ao executar múltiplas consultas: {e}")
            self.connection.rollback()
            raise

    def insert(self, query):
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except psycopg2.Error as e:
            print(f'Erro ao executar a consulta: {str(e)}')
            print(query)

    def insert_table(self, table, columns, values):        
        try:
            with self.connection.cursor() as cursor:
                columns_str = ', '.join(columns)  # Concatena os nomes das colunas
                placeholders = ', '.join(['%s'] * len(values))  # Gera placeholders para os valores
                query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
                cursor.execute(query, values)
                self.connection.commit()
                print("Dados inseridos com sucesso!")
        except psycopg2.Error as e:
            print(f"Erro ao inserir na tabela: {e}")
            self.connection.rollback()
            raise

if __name__ == "__main__":
    # Informações da conexão
    db_config = {
        "host": "localhost",
        "database": "contem",
        "user": "postgres",
        "password": "C@med2024",
        "port": 5432
    }

    # Instancia a classe
    db = PostgresConnection(**db_config)

    try:
        # Conecta ao banco
        db.connect()

        db.insert_table(
            table="motivo_canc_susp",
            columns=["nome_motivo"],
            values=["Teste de Inserção"]
        )

        # Verifica o resultado
        results = db.execute_query("SELECT * FROM motivo_canc_susp")
        print(results)

    finally:
        # Fecha a conexão
        db.close()
