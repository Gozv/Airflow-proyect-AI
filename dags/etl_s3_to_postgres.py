from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.models import Variable
import pandas as pd
import logging

def _extract_from_s3(**context):
    s3_hook = S3Hook(aws_conn_id='aws_default')
    key = f"data/{context['ds']}.csv"
    file_name = s3_hook.download_file(key=key, bucket_name=Variable.get("S3_BUCKET"))
    return file_name

def _transform_data(**context):
    ti = context['ti']
    file_name = ti.xcom_pull(task_ids='extract_from_s3')
    
    df = pd.read_csv(file_name)
    
    # Business logic
    df['total'] = df['quantity'] * df['unit_price']
    df['processed_at'] = datetime.now()
    
    processed_file = f"/tmp/processed_{context['ds_nodash']}.csv"
    df.to_csv(processed_file, index=False)
    return processed_file

def _load_to_postgres(**context):
    postgres_hook = PostgresHook(postgres_conn_id='postgres_default')
    ti = context['ti']
    processed_file = ti.xcom_pull(task_ids='transform_data')
    
    df = pd.read_csv(processed_file)
    df.to_sql(
        name='sales_data',
        con=postgres_hook.get_sqlalchemy_engine(),
        if_exists='append',
        index=False
    )
    logging.info(f"Loaded {len(df)} records to PostgreSQL")

with DAG(
    dag_id='s3_to_postgres_etl',
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
    default_args={
        'retries': 3,
        'retry_delay': timedelta(minutes=5),
        'on_failure_callback': lambda context: send_alert(context)
    },
    tags=['ETL', 'production']
) as dag:
    
    extract = PythonOperator(
        task_id='extract_from_s3',
        python_callable=_extract_from_s3,
        provide_context=True
    )
    
    transform = PythonOperator(
        task_id='transform_data',
        python_callable=_transform_data,
        provide_context=True
    )
    
    load = PythonOperator(
        task_id='load_to_postgres',
        python_callable=_load_to_postgres,
        provide_context=True
    )
    
    data_quality_check = SQLColumnCheckOperator(
        task_id='data_quality_check',
        conn_id='postgres_default',
        table='sales_data',
        column_mapping={
            "total": {
                "min": {"geq_to": 0},
                "max": {"leq_to": 10000}
            }
        }
    )
    
    extract >> transform >> load >> data_quality_check