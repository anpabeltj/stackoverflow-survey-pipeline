# 📊 Stack Overflow Developer Survey Pipeline

A data pipeline project that processes the **Stack Overflow Developer Survey 2023** using **dbt (data build tool)**. It extracts, loads, and transforms survey data to make it ready for analysis.

---

## 🗂️ What This Project Does

1. **Extract** — A Python script reads the raw Stack Overflow survey CSV and samples 5,000 responses with a selected set of meaningful columns.
2. **Load** — The sampled data is stored as a dbt seed, acting as the raw source layer.
3. **Transform** — A dbt staging model cleans and standardizes the data (renaming columns, handling nulls, fixing data types).

---

## 📁 Project Structure

```
stackoverflow_survey/
├── extract.py              # Python script to extract and sample raw survey data
├── seeds/
│   └── raw_survey.csv      # Sampled survey data (5,000 rows), loaded as dbt seed
├── models/
│   ├── schema.yml          # Column descriptions and data tests
│   └── staging/
│       └── stg_survey.sql  # Staging model: cleaned and renamed survey data
├── dbt_project.yml         # dbt project configuration
└── README.md
```

---

## 📋 Data Source

The raw data comes from the **Stack Overflow Developer Survey 2023** (publicly available dataset).

The Python script (`extract.py`) selects the following columns from the full survey:

| Column                   | Description                                  |
| ------------------------ | -------------------------------------------- |
| `ResponseId`             | Unique identifier per respondent             |
| `Age`                    | Age group of the respondent                  |
| `Country`                | Country of residence                         |
| `EdLevel`                | Highest education level                      |
| `Employment`             | Employment status                            |
| `RemoteWork`             | Work arrangement (remote, hybrid, in-person) |
| `DevType`                | Type of developer role                       |
| `YearsCodePro`           | Years of professional coding experience      |
| `OrgSize`                | Size of the respondent's organization        |
| `ConvertedCompYearly`    | Annual compensation in USD                   |
| `Currency`               | Currency of reported compensation            |
| `LanguageHaveWorkedWith` | Programming languages used                   |
| `DatabaseHaveWorkedWith` | Databases used                               |
| `AISelect`               | Whether the respondent uses AI tools         |
| `AISent`                 | Sentiment toward AI tools                    |
| `AIBen`                  | Perceived benefit of AI tools                |

---

## 🔧 Models

### `stg_survey` (Staging Layer)

**Materialization:** View

This model reads from the `raw_survey` seed and applies the following transformations:

- Renames all columns to snake_case
- Filters out rows where `ResponseId`, `Country`, or `Employment` is null
- Converts `ConvertedCompYearly` to an integer, replacing `'NA'` with `NULL`

**Data tests applied:**

- `response_id`: must be unique
- `response_id`, `employment`, `country`: warned when null values are found

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- dbt (configured with the `stackoverflow_survey` profile)
- A compatible database (PostgreSQL or DuckDB)

### 1. Extract the raw data

Run the Python script to generate the seed file:

```bash
python extract.py
```

This reads `survey_results_public.csv` from the project root and writes a 5,000-row sample to `seeds/raw_survey.csv`.

### 2. Load the seed into the database

```bash
dbt seed
```

### 3. Run the models

```bash
dbt run
```

### 4. Run data tests

```bash
dbt test
```

---

## ⚙️ Configuration

The dbt project profile is named `stackoverflow_survey`. Make sure your `~/.dbt/profiles.yml` file contains a matching profile pointing to your database.

Model materialization defaults:

| Layer     | Type  |
| --------- | ----- |
| `staging` | View  |
| `marts`   | Table |

---

## 📌 Notes

- The `survey_results_public.csv` raw file is not committed to the repository (it is listed in `.gitignore`). You need to download it separately from the Stack Overflow survey website and place it in the project root before running `extract.py`.
- The seed file `raw_survey.csv` contains only 5,000 randomly sampled rows (using `random_state=42` for reproducibility).
