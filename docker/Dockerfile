FROM apache/airflow:2.7.2

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev && \
    apt-get clean

USER airflow
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --user

COPY scripts/ /opt/airflow/scripts/
RUN chmod +x /opt/airflow/scripts/*.sh