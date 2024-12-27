from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Importe a função iniciar_navegacao do seu script Selenium
from Extrator_bdcontratos3 import iniciar_navegacao

# Configuração padrão da DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 12, 16),  # Ajuste a data de início conforme necessário
    'email': ['jeffersonsales@pharosconsultoria.com.br'],  # Email de notificação
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(seconds=30),
}

# Criação da DAG
with DAG( 
    dag_id='BONECO_DO_CONTRATO',
    default_args=default_args,
    schedule_interval=None,  # Definido como manual
    catchup=False,  # Evita execução retroativa de DAGs passadas
    tags=['selenium', 'extrator'],
) as dag:

    # Definição da tarefa que chama o script Selenium
    extrair_contratos = PythonOperator(
        task_id='extrair_contratos',
        python_callable=iniciar_navegacao,  # Função do seu script
        execution_timeout=timedelta(minutes=60)
    )
