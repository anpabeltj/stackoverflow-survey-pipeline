import json
import os

import joblib
import pandas as pd
from dotenv import load_dotenv
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sqlalchemy import create_engine

FEATURES = [
    "country",
    "age",
    "education_level",
    "dev_type",
    "employment",
    "org_size",
    "remote_work",
    "experience_level",
]
TARGET = "salary_level"
MIN_CATEGORY_COUNT = 30
ARTIFACT_DIR = os.path.join(os.path.dirname(__file__), "artifacts")


def load_data():
    load_dotenv()
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}")
    return pd.read_sql("select * from analytics.ml_salary_features", engine)


def group_rare_categories(df, column, min_count):
    # Rare values (e.g. small countries) become "Other" so the model is not overfitting on a handful of rows
    counts = df[column].value_counts()
    keep = counts[counts >= min_count].index
    df.loc[~df[column].isin(keep), column] = "Other"
    return df


def prepare(df):
    df = df.copy()
    for column in FEATURES:
        df[column] = df[column].fillna("Unknown")
        df = group_rare_categories(df, column, MIN_CATEGORY_COUNT)
    return df


def build_model():
    preprocessor = ColumnTransformer(
        transformers=[("categorical", OneHotEncoder(handle_unknown="ignore"), FEATURES)]
    )
    classifier = RandomForestClassifier(
        n_estimators=300,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=42,
    )
    return Pipeline(steps=[("preprocess", preprocessor), ("classifier", classifier)])


def main():
    df = prepare(load_data())
    print(f"Training rows: {len(df)}")

    x = df[FEATURES]
    y = df[TARGET]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, stratify=y, random_state=42
    )

    model = build_model()
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    # Baseline: always predicting the most common class
    baseline_accuracy = y_test.value_counts(normalize=True).max()

    metrics = {
        "rows": len(df),
        "accuracy": round(accuracy_score(y_test, predictions), 3),
        "macro_f1": round(f1_score(y_test, predictions, average="macro"), 3),
        "baseline_accuracy": round(float(baseline_accuracy), 3),
        "report": classification_report(y_test, predictions, output_dict=True),
    }

    # Allowed dropdown values for the app
    options = {}
    for column in FEATURES:
        options[column] = sorted(df[column].unique().tolist())

    os.makedirs(ARTIFACT_DIR, exist_ok=True)
    joblib.dump(model, os.path.join(ARTIFACT_DIR, "salary_model.joblib"))
    with open(os.path.join(ARTIFACT_DIR, "metrics.json"), "w") as file:
        json.dump(metrics, file, indent=2)
    with open(os.path.join(ARTIFACT_DIR, "options.json"), "w") as file:
        json.dump(options, file, indent=2)

    print(f"Accuracy: {metrics['accuracy']} (baseline {metrics['baseline_accuracy']})")
    print(f"Macro F1: {metrics['macro_f1']}")
    print(f"Saved model to {ARTIFACT_DIR}")


if __name__ == "__main__":
    main()