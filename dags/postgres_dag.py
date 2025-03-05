from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1)
}

with DAG(
    'postgres_operations',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
) as dag:

    create_table = PostgresOperator(
        task_id='crear_tabla',
        postgres_conn_id='postgres_default',
        sql="""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(50),
            email VARCHAR(100)
        );
        """
    )

    insert_data = PostgresOperator(
        task_id='insertar_datos',
        postgres_conn_id='postgres_default',
        sql="""
        INSERT INTO usuarios (nombre, email)
        VALUES ('Juan Perez', 'juan@example.com');
        """
    )

    create_table >> insert_data