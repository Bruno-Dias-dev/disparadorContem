import psycopg2
from psycopg2 import sql

def create_database():
    try:
        # Conexão com o banco de dados PostgreSQL
        connection = psycopg2.connect(
            database="BD_Dom",
            user="postgres",
            password="pharos",
            host="localhost",
            port=5432
        )

        connection.autocommit = True
        cursor = connection.cursor()

        # Lista de comandos SQL para criar as tabelas
        commands = [
           """CREATE TABLE grupo_produtor (
                id_grupo_produtor SERIAL PRIMARY KEY,
                nome VARCHAR(255),
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",

            """CREATE TABLE superior (
                id_superior SERIAL PRIMARY KEY,
                nome VARCHAR(255),
                cpf_cnpj VARCHAR(20),
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",

            """CREATE TABLE supervisor (
                id_supervisor SERIAL PRIMARY KEY,
                nome VARCHAR(255),
                cpf_cnpj VARCHAR(20),
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",

            """CREATE TABLE corretora (
                id_corretora SERIAL PRIMARY KEY,
                nome VARCHAR(255),
                angariador VARCHAR(255),
                gerente VARCHAR(255),
                filial VARCHAR(255),
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",

            '''CREATE TABLE cliente (
                id_cliente SERIAL PRIMARY KEY,
                codigo_cliente VARCHAR(255),
                nome VARCHAR(255),
                marca_optica_titular VARCHAR(255),
                cpf_titular VARCHAR(20),
                endereco VARCHAR(255),
                tipo_cliente VARCHAR(255),
                nome_mae VARCHAR(255),
                nome_pai VARCHAR(255),
                sexo CHAR(1),
                nascimento DATE,
                idade INT,
                status VARCHAR(255),
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',

            '''CREATE TABLE operadora (
                id_operadora SERIAL PRIMARY KEY,
                nome VARCHAR(255),
                cnpj VARCHAR(20),
                pessoa_juridica BOOLEAN,
                telefone_atendimento VARCHAR(20),
                celular_atendimento VARCHAR(20),
                email_atendimento VARCHAR(255),
                status VARCHAR(255),
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',

            '''CREATE TABLE plano (
                id_plano SERIAL PRIMARY KEY,
                nome VARCHAR(255),
                acomodacao VARCHAR(255),
                opcionais VARCHAR(255),
                matricula VARCHAR(255),
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',

            '''CREATE TABLE convenio (
                id_convenio SERIAL PRIMARY KEY,
                grupo VARCHAR(255),
                sub_estipulante VARCHAR(255),
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',

            """CREATE TABLE produtor (
                id_produtor SERIAL PRIMARY KEY,
                codigo VARCHAR(255),
                nome VARCHAR(255),
                cpf_cnpj VARCHAR(20),
                grupo_produtor_id INT REFERENCES grupo_produtor(id_grupo_produtor),
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",

            '''CREATE TABLE responsavel_financeiro (
                id_responsavel_financeiro SERIAL PRIMARY KEY,
                nome VARCHAR(255),
                cpf_cnpj VARCHAR(20),
                contato VARCHAR(255),
                id_cliente INT REFERENCES cliente(id_cliente),
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',
            '''CREATE TABLE IF NOT EXISTS relatorio_contratos (
                id_relatorio_contratos SERIAL PRIMARY KEY,
                codigo_contrato VARCHAR(255),
                numero_proposta VARCHAR(255),
                status_contrato VARCHAR(255),
                data_cancelamento DATE,
                motivo_cancelamento VARCHAR(255),
                motivo_suspensao VARCHAR(255),
                dia_vencimento INT,
                data_vigencia DATE,
                inicio_vigencia DATE,
                cliente_id INT REFERENCES cliente(id_cliente),
                status VARCHAR(255),
                data_assinatura DATE,
                data_suspensao DATE,
                data_exclusao DATE,
                data_inclusao DATE,
                produtor_id INT REFERENCES produtor(id_produtor),
                acao_judicial BOOLEAN,
                data_prox_reajuste DATE,
                mes_reajuste VARCHAR(255),
                plano_id INT REFERENCES plano(id_plano),
                qtd_vidas INT,
                debito_automatico BOOLEAN,
                conta_debito_automatico VARCHAR(255),
                corretor_id INT REFERENCES corretora(id_corretora),
                forma_ajuste VARCHAR(255),
                ajuste VARCHAR(255),
                prazo_ajuste VARCHAR(255),
                valor_venda NUMERIC(10,2),
                bloqueio_comissao BOOLEAN,
                pendencias VARCHAR(255),
                resp_fin_id INT REFERENCES responsavel_financeiro(id_responsavel_financeiro),
                observacao TEXT,
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',

            '''CREATE TABLE estipulante (
                id_estipulante SERIAL PRIMARY KEY,
                sub_estipulante_id INT REFERENCES convenio(id_convenio),
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',

            '''CREATE TABLE faturas (
                id_fatura SERIAL PRIMARY KEY,
                contrato_id INT REFERENCES relatorio_contratos(id_relatorio_contratos),
                codigo_fatura VARCHAR(255),
                dia_vencimento INT,
                vencimento DATE,
                valor NUMERIC(10,2),
                data_pagamento DATE,
                data_emissao DATE,
                status VARCHAR(255),
                operadora_id INT REFERENCES operadora(id_operadora),
                convenio_id INT REFERENCES convenio(id_convenio),
                grupo_id INT REFERENCES grupo_produtor(id_grupo_produtor),
                estipulante INT REFERENCES estipulante(id_estipulante),
                sub_estipulante INT REFERENCES convenio(id_convenio),
                data_saldo DATE,
                superior_id INT REFERENCES superior(id_superior),
                supervisor_id INT REFERENCES supervisor(id_supervisor),
                alerta VARCHAR(255),
                cliente_id INT REFERENCES cliente(id_cliente),
                produtor_id INT REFERENCES produtor(id_produtor),
                data_cancelamento DATE,
                motivo_cancelamento VARCHAR(255),
                motivo_baixa VARCHAR(255),
                parcela INT,
                mes_competencia INT,
                ano_competencia INT,
                rubrica VARCHAR(255),
                descricao TEXT,
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',

            '''CREATE TABLE relatorio_inadimplencia (
                id_relatorio_inadimplencia SERIAL PRIMARY KEY,
                contrato_id INT REFERENCES relatorio_contratos(id_relatorio_contratos),
                codigo_contrato VARCHAR(255),
                numero_proposta VARCHAR(255),
                nome_titular VARCHAR(255),
                data_spc DATE,
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',

            '''CREATE TABLE contato (
                id_contato SERIAL PRIMARY KEY,
                cliente_id INT REFERENCES cliente(id_cliente),
                telefone VARCHAR(20),
                celular VARCHAR(20),
                email_principal VARCHAR(255),
                email_secundario VARCHAR(255),
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',

            '''CREATE TABLE endereco (
                id_endereco SERIAL PRIMARY KEY,
                cliente_id INT REFERENCES cliente(id_cliente),
                logradouro VARCHAR(255),
                numero VARCHAR(10),
                complemento VARCHAR(255),
                bairro VARCHAR(255),
                municipio VARCHAR(255),
                uf CHAR(2),
                cep VARCHAR(10),
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',

            '''CREATE TABLE cliente_cobranca (
                id_cliente_cobranca SERIAL PRIMARY KEY,
                cliente_id INT REFERENCES cliente(id_cliente),
                fatura_id INT REFERENCES faturas(id_fatura),
                data_spc DATE,
                data_serasa DATE,
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',

            '''CREATE TABLE cobrancas (
                id_cobranca SERIAL PRIMARY KEY,
                fatura_id INT REFERENCES faturas(id_fatura),
                codigo VARCHAR(255),
                valor_pago NUMERIC(10,2),
                valor_juros NUMERIC(10,2),
                valor_multa NUMERIC(10,2),
                mensagem TEXT,
                indicador_pro_rata BOOLEAN,
                tipo_correspondencia VARCHAR(255),
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''',

            '''CREATE TABLE fatura_financeiro (
                id_fatura_financeiro SERIAL PRIMARY KEY,
                fatura_id INT REFERENCES faturas(id_fatura),
                valor_net NUMERIC(10,2),
                valor_cobranca NUMERIC(10,2),
                valor_pago_fatura NUMERIC(10,2),
                valor_juros NUMERIC(10,2),
                valor_multa NUMERIC(10,2),
                spread NUMERIC(10,2),
                observacoes TEXT,
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )'''
        ]

        # Executa cada comando para criar as tabelas
        for command in commands:
            cursor.execute(command)
            print(f"Tabela criada com sucesso: {command.split()[2]}")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Erro ao criar o banco de dados: {error}")
    finally:
        # Fecha a conexão
        if 'connection' in locals() and connection:
            cursor.close()
            connection.close()
            print("Conexão ao banco de dados encerrada.")

if __name__ == "__main__":
    create_database()
