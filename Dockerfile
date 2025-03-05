FROM apache/airflow:2.7.2

USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev

USER airflow
RUN pip install --upgrade pip
RUN pip install \
    apache-airflow-providers-postgres \
    apache-airflow-providers-amazon \
    apache-airflow-providers-http \
    requests