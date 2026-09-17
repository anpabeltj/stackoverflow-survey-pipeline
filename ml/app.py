import json
import os

import joblib
import pandas as pd
import streamlit as st

ARTIFACT_DIR = os.path.join(os.path.dirname(__file__), "artifacts")
SALARY_ORDER = ["Entry", "Mid", "Senior"]
SALARY_RANGES = {
    "Entry": "below \\$50K / year",
    "Mid": "\\$50K to \\$100K / year",
    "Senior": "above \\$100K / year",
}
SALARY_ICONS = {"Entry": "🌱", "Mid": "📈", "Senior": "🏆"}
LABELS = {
    "country": "Country",
    "age": "Age",
    "education_level": "Education level",
    "dev_type": "Developer role",
    "employment": "Employment",
    "org_size": "Organization size",
    "remote_work": "Work arrangement",
    "experience_level": "Experience level",
}


@st.cache_resource
def load_artifacts():
    model = joblib.load(os.path.join(ARTIFACT_DIR, "salary_model.joblib"))
    with open(os.path.join(ARTIFACT_DIR, "options.json")) as file:
        options = json.load(file)
    with open(os.path.join(ARTIFACT_DIR, "metrics.json")) as file:
        metrics = json.load(file)
    return model, options, metrics


st.set_page_config(page_title="Developer Salary Level Predictor", page_icon="💼", layout="centered")

# App starts before the DAG has run, so show a message instead of crashing
if not os.path.exists(os.path.join(ARTIFACT_DIR, "salary_model.joblib")):
    st.info("Model not trained yet. Trigger the stackoverflow_survey_pipeline DAG in Airflow, then refresh this page.")
    st.stop()

model, options, metrics = load_artifacts()

# Header
st.title("💼 Developer Salary Level Predictor")
st.caption("Machine learning model trained on the Stack Overflow Developer Survey 2023")

# Salary level legend
legend_columns = st.columns(3)
for index, level in enumerate(SALARY_ORDER):
    with legend_columns[index]:
        with st.container(border=True):
            st.markdown(f"**{SALARY_ICONS[level]} {level}**")
            st.caption(SALARY_RANGES[level])

# Input form
with st.form("profile_form"):
    st.subheader("Developer profile")
    inputs = {}
    left, right = st.columns(2)
    column_names = list(LABELS.keys())
    for index, column in enumerate(column_names):
        container = left if index % 2 == 0 else right
        inputs[column] = container.selectbox(LABELS[column], options[column])
    submitted = st.form_submit_button("Predict salary level", type="primary", use_container_width=True)

# Prediction result
if submitted:
    row = pd.DataFrame([inputs])
    prediction = model.predict(row)[0]
    probabilities = model.predict_proba(row)[0]

    probability_by_level = {}
    for level, probability in zip(model.classes_, probabilities):
        probability_by_level[level] = float(probability)

    with st.container(border=True):
        st.subheader(f"{SALARY_ICONS[prediction]} Predicted: {prediction}")
        st.caption(f"{SALARY_RANGES[prediction]}, with {probability_by_level[prediction]:.0%} confidence")

        for level in SALARY_ORDER:
            probability = probability_by_level[level]
            label_col, bar_col, value_col = st.columns([1, 5, 1], vertical_alignment="center")
            label_col.markdown(f"**{level}**")
            bar_col.progress(probability)
            value_col.markdown(f"{probability:.0%}")

# Model performance
st.subheader("Model performance")
improvement = metrics["accuracy"] - metrics["baseline_accuracy"]
metric_columns = st.columns(3)
with metric_columns[0]:
    with st.container(border=True):
        st.metric("Accuracy", f"{metrics['accuracy']:.1%}", f"+{improvement:.1%} vs baseline")
with metric_columns[1]:
    with st.container(border=True):
        st.metric("Macro F1", f"{metrics['macro_f1']:.3f}")
with metric_columns[2]:
    with st.container(border=True):
        st.metric("Baseline", f"{metrics['baseline_accuracy']:.1%}")

with st.expander("About this model"):
    st.markdown(
        f"""
- **Algorithm:** Random Forest classifier (scikit-learn)
- **Training data:** {metrics['rows']:,} respondents with a known salary
- **Features:** country, age, education, role, employment, organization size, work arrangement, experience
- **Baseline:** always predicting the most common salary level
- **Note:** salaries are converted to USD, so country has a strong effect. Treat predictions as a rough estimate.
"""
    )