FROM apache/airflow:2.10.5-python3.11

# One image for Airflow and the Streamlit app.
# Pipeline libraries (pandas, SQLAlchemy 2, dbt, scikit-learn, streamlit) live in their own venv
# so they do not clash with Airflow's own dependencies.
COPY requirements.txt /tmp/requirements.txt
RUN python -m venv /opt/airflow/venv_pipeline \
    && /opt/airflow/venv_pipeline/bin/pip install --no-cache-dir -r /tmp/requirements.txt