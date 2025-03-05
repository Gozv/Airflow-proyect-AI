from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1
}

def _print_hello():
    print("¡Tarea ejecutada con éxito!")

with DAG(
    'ejemplo_basico',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    task1 = BashOperator(
        task_id='imprimir_fecha',
        bash_command='date'
    )

    task2 = BashOperator(
        task_id='dormir',
        bash_command='sleep 5'
    )

    task3 = PythonOperator(
        task_id='saludar',
        python_callable=_print_hello
    )

    task1 >> task2 >> task3