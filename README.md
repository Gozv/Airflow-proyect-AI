# Airflow ETL Pipeline

![Airflow Version](https://img.shields.io/badge/Airflow-2.7.2-blue)
![Docker](https://img.shields.io/badge/Docker-20.10%2B-blue)

Pipeline ETL profesional para procesamiento de datos con:

- Extracción desde S3
- Transformación con Pandas
- Carga a PostgreSQL
- Validación de datos
- Monitoreo integrado

🛠️ Features
Modern Data Stack

Airflow 2.0 TaskFlow API

XCom backend with S3

Python 3.10 type hints

Data Quality

Column-level checks

Statistical validation

Automated reporting (Markdown + S3)

DevOps Ready

Dockerized environment

Kubernetes-ready configuration

Automated testing framework

Security

Fernet key encryption

Secrets management with .env

RBAC-ready configuration


## 🚀 Instalación

1. Clonar repositorio
2. Configurar `.env` basado en `env.example`
3. Ejecutar:


## 📂 Project Structure

```bash
airflow-project/
├── dags/                   # Pipeline definitions
│   ├── etl_s3_to_postgres.py    # Main ETL workflow
│   ├── data_validation_dag.py   # Data quality checks
│   ├── api_etl_dag.py           # API ingestion pipeline
│   └── ...
├── config/                # Environment configuration
├── docker/                # Docker infrastructure
├── tests/                 # Unit and integration tests
├── scripts/               # Automation scripts
├── .gitignore            # Version control config
├── docker-compose.yml     # Local orchestration
├── Makefile               # Build automation
└── README.md              # Project documentation
