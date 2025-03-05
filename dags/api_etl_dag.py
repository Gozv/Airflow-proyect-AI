from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import Variable
import requests
import json
import logging

def _extract_api_data(**context):
    api_url = Variable.get("API_ENDPOINT")
    headers = {"Authorization": f"Bearer {Variable.get('API_KEY')}"}
    
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    context['ti'].xcom_push(key='api_data', value=data)
    return data

def _transform_api_data(**context):
    raw_data = context['ti'].xcom_pull(task_ids='extract_api_data', key='api_data')
    
    # Business transformations
    transformed = []
    for item in raw_data['results']:
        transformed.append({
            'user_id': item['id'],
            'username': item['username'],
            'registration_date': item['joinedAt'],
            'last_activity': datetime.now().isoformat()
        })
    
    context['ti'].xcom_push(key='transformed_data', value=transformed)
    return transformed

def _load_to_postgres(**context):
    hook = PostgresHook(postgres_conn_id='postgres_default')
    data = context['ti'].xcom_pull(task_ids='transform_api_data', key='transformed_data')
    
    df = pd.DataFrame(data)
    df.to_sql(
        name='user_activity',
        con=hook.get_sqlalchemy_engine(),
        if_exists='append',
        index=False
    )
    logging.info(f"Loaded {len(df)} user records")

with DAG(
    dag_id='api_user_etl',
    schedule_interval=timedelta(hours=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
    default_args={
        'retries': 3,
        'retry_delay': timedelta(minutes=5),
        'on_failure_callback': send_slack_alert
    },
    tags=['API', 'hourly']
) as dag:

    extract = PythonOperator(
        task_id='extract_api_data',
        python_callable=_extract_api_data,
        provide_context=True
    )

    transform = PythonOperator(
        task_id='transform_api_data',
        python_callable=_transform_api_data,
        provide_context=True
    )

    load = PythonOperator(
        task_id='load_to_postgres',
        python_callable=_load_to_postgres,
        provide_context=True
    )

    validate_data = SQLColumnCheckOperator(
        task_id='validate_user_data',
        conn_id='postgres_default',
        table='user_activity',
        column_mapping={
            "user_id": {"unique_check": {"geq_to": 0