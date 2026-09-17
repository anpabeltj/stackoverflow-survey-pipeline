from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

# Project folder is mounted here by docker-compose.airflow.yml
PROJECT_DIR = "/opt/airflow/project"
# Separate venv so pipeline libraries (SQLAlchemy 2, dbt) do not clash with Airflow's own dependencies
VENV_BIN = "/opt/airflow/venv_pipeline/bin"

default_args = {
    "owner": "patra",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="stackoverflow_survey_pipeline",
    description="Extract, load, dbt transform, and train the salary model",
    start_date=datetime(2026, 1, 1),
    schedule=None,  # survey is a static yearly file, so trigger manually
    catchup=False,
    default_args=default_args,
    tags=["stackoverflow", "dbt", "ml"],
) as dag:

    check_source_file = BashOperator(
        task_id="check_source_file",
        bash_command=f"test -f {PROJECT_DIR}/survey_results_public.csv",
        retries=0,
    )

    extract = BashOperator(
        task_id="extract",
        bash_command=f"cd {PROJECT_DIR} && mkdir -p data && {VENV_BIN}/python extract.py",
    )

    load = BashOperator(
        task_id="load",
        bash_command=f"cd {PROJECT_DIR} && {VENV_BIN}/python load.py",
    )

    dbt_run_staging = BashOperator(
        task_id="dbt_run_staging",
        bash_command=f"cd {PROJECT_DIR} && {VENV_BIN}/dbt run --select path:models/staging",
    )

    dbt_test_staging = BashOperator(
        task_id="dbt_test_staging",
        bash_command=f"cd {PROJECT_DIR} && {VENV_BIN}/dbt test --select path:models/staging",
    )

    dbt_run_marts = BashOperator(
        task_id="dbt_run_marts",
        bash_command=f"cd {PROJECT_DIR} && {VENV_BIN}/dbt run --select path:models/marts",
    )

    dbt_test_marts = BashOperator(
        task_id="dbt_test_marts",
        bash_command=f"cd {PROJECT_DIR} && {VENV_BIN}/dbt test --select path:models/marts",
    )

    train_model = BashOperator(
        task_id="train_model",
        bash_command=f"cd {PROJECT_DIR} && {VENV_BIN}/python ml/train.py",
    )

    (
        check_source_file
        >> extract
        >> load
        >> dbt_run_staging
        >> dbt_test_staging
        >> dbt_run_marts
        >> dbt_test_marts
        >> train_model
    )