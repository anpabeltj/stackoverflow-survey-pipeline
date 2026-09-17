import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}")

# Keep everything as raw text, type casting happens in dbt staging
df = pd.read_csv("data/raw_survey.csv", dtype=str)

with engine.begin() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))
    # CASCADE removes dependent dbt views, dbt run rebuilds them
    conn.execute(text("DROP TABLE IF EXISTS raw.raw_survey CASCADE"))

df.to_sql("raw_survey", engine, schema="raw", if_exists="replace", index=False, chunksize=1000)

print(f"Loaded {len(df)} rows into raw.raw_survey")