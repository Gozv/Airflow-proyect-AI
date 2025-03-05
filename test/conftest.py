import pytest
from unittest.mock import Mock, patch
from airflow.models import DagBag, Connection
from airflow.settings import Session

@pytest.fixture(scope="session", autouse=True)
def mock_connections():
    """Mock all external connections for testing"""
    with patch('airflow.hooks.base.BaseHook.get_connection') as mock_get:
        # Mock PostgreSQL connection
        postgres_conn = Connection(
            conn_id='postgres_default',
            conn_type='postgres',
            host='localhost',
            login='test',
            password='test',
            port=5432
        )
        
        # Mock AWS connection
        aws_conn = Connection(
            conn_id='aws_default',
            conn_type='aws',
            extra={
                "aws_access_key_id": "test_key",
                "aws_secret_access_key": "test_secret",
                "region_name": "us-east-1"
            }
        )
        
        mock_get.side_effect = lambda conn_id: {
            'postgres_default': postgres_conn,
            'aws_default': aws_conn
        }.get(conn_id)
        
        yield

@pytest.fixture(scope="session")
def dag_bag():
    """Initialize DagBag for testing"""
    return DagBag(dag_folder='dags/', include_examples=False)

@pytest.fixture(autouse=True)
def clean_db():
    """Clean Airflow metadata database before each test"""
    from airflow.utils.db import resetdb
    resetdb()