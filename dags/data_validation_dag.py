from datetime import datetime
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.common.sql.operators.sql import SQLColumnCheckOperator
from airflow.operators.python import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
import pandas as pd

def _generate_validation_report(**context):
    hook = PostgresHook(postgres_conn_id='postgres_default')
    df = hook.get_pandas_df("SELECT * FROM validation_results")
    
    # Generar reporte en formato markdown
    report = f"""
    ## Validation Report - {context['ds']}
    
    ### Summary:
    - Total Tests: {len(df)}
    - Passed: {df[df['status'] == 'SUCCESS'].shape[0]}
    - Failed: {df[df['status'] == 'FAILED'].shape[0]}
    
    ### Details:
    {df.to_markdown(index=False)}
    """
    
    # Guardar reporte en S3
    s3_hook = S3Hook(aws_conn_id='aws_default')
    s3_hook.load_string(
        string_data=report,
        key=f"reports/{context['ds_nodash']}_validation.md",
        bucket_name=Variable.get("S3_BUCKET"),
        replace=True
    )

with DAG(
    dag_id='data_validation',
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
    default_args={
        'retries': 2,
        'retry_delay': timedelta(minutes=3)
    },
    tags=['validation', 'monitoring']
) as dag:

    create_validation_table = PostgresOperator(
        task_id='create_validation_table',
        sql="""
        CREATE TABLE IF NOT EXISTS validation_results (
            test_name VARCHAR(255),
            status VARCHAR(50),
            error_message TEXT,
            execution_date TIMESTAMP
        );
        """
    )

    check_sales_data = SQLColumnCheckOperator(
        task_id='check_sales_data