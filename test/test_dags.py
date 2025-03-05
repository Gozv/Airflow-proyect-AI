import pytest
from airflow.models import DagBag

@pytest.fixture(scope="session")
def dag_bag():
    return DagBag(dag_folder="dags/", include_examples=False)

def test_dag_loading(dag_bag):
    assert not dag_bag.import_errors

def test_dag_structure():
    dag_id = 's3_to_postgres_etl'
    dag = dag_bag.get_dag(dag_id)
    
    assert dag is not None
    assert len(dag.tasks) == 4
    assert set(task.task_id for task in dag.tasks) == {
        'extract_from_s3',
        'transform_data',
        'load_to_postgres',
        'data_quality_check'
    }