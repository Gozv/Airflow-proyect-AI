from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import requests
from datetime import datetime

def _download_and_upload(**kwargs):
    # Descargar datos de API
    response = requests.get('https://jsonplaceholder.typicode.com/todos/1')
    data = response.json()
    
    # Subir a S3
    s3_hook = S3Hook(aws_conn_id='aws_s3_conn')
    s3_hook.load_string(
        string_data=str(data),
        key=f'data/{kwargs["ds"]}.json',
        bucket_name='mi-bucket',
        replace=True
    )

with DAG(
    's3_etl',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:
    
    upload_task = PythonOperator(
        task_id='upload_to_s3',
        python_callable=_download_and_upload,
        provide_context=True
    )