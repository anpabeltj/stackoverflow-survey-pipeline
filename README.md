# 📊 Stack Overflow Developer Survey Pipeline

A data pipeline project that processes the **Stack Overflow Developer Survey 2023** using **dbt (data build tool)**. It extracts, loads, and transforms survey data to make it ready for analysis.

---

## 🗂️ What This Project Does

1. **Extract** — A Python script reads the raw Stack Overflow survey CSV and samples 5,000 responses with a selected set of meaningful columns.
2. **Load** — The sampled data is stored as a dbt seed, acting as the raw source layer.
3. **Transform** — dbt models clean, standardize, and aggregate the data across two layers:
   - **Staging** — renames columns, filters nulls, and fixes data types
   - **Marts** — produces ready-to-use analytical tables on developer profiles and technology popularity

---

## 📁 Project Structure

```
stackoverflow_survey/
├── extract.py                        # Python script to extract and sample raw survey data
├── seeds/
│   └── raw_survey.csv                # Sampled survey data (5,000 rows), loaded as dbt seed
├── models/
│   ├── staging/
│   │   ├── schema.yml                # Column descriptions and data tests
│   │   └── stg_survey.sql            # Staging model: cleaned and renamed survey data
│   └── marts/
│       ├── developer/
│       │   └── developer_profile.sql # Developer demographics and experience level
│       └── tech/
│           ├── language_popularity.sql   # Most used programming languages
│           └── database_popularity.sql   # Most used databases
├── dbt_project.yml                   # dbt project configuration
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

### Staging Layer

#### `stg_survey`

**Materialization:** View

This model reads from the `raw_survey` seed and applies the following transformations:

- Renames all columns to snake_case
- Filters out rows where `ResponseId`, `Country`, or `Employment` is null
- Converts `ConvertedCompYearly` to an integer, replacing `'NA'` with `NULL`

**Data tests applied:**

- `response_id`: must be unique
- `response_id`, `employment`, `country`: warned when null values are found

---

### Marts Layer

All marts models are materialized as **tables** and built on top of `stg_survey`.

#### `developer_profile`

**Location:** `models/marts/developer/developer_profile.sql`

Produces a profile of each survey respondent enriched with two derived fields:

| Column             | Description                                                                                          |
| ------------------ | ---------------------------------------------------------------------------------------------------- |
| `age`              | Age group of the respondent                                                                          |
| `country`          | Country of residence                                                                                 |
| `dev_type`         | Type of developer role                                                                               |
| `employment`       | Employment status                                                                                    |
| `education_level`  | Highest education level                                                                              |
| `remote_work`      | Work arrangement                                                                                     |
| `org_size`         | Organization size                                                                                    |
| `salary_level`     | Bucketed salary: `Entry` (below $50K), `Mid` ($50K to $100K), `Senior` (above $100K), or `Unknown`   |
| `experience_level` | Bucketed experience: `Junior` (0 to 3 yrs), `Mid` (4 to 7 yrs), `Senior` (above 7 yrs), or `Unknown` |

#### `language_popularity`

**Location:** `models/marts/tech/language_popularity.sql`

Counts how many developers have worked with each programming language. Languages are split from the multi-value `LanguageHaveWorkedWith` field.

| Column                 | Description                       |
| ---------------------- | --------------------------------- |
| `programming_language` | Name of the programming language  |
| `developer_count`      | Number of respondents who used it |

#### `database_popularity`

**Location:** `models/marts/tech/database_popularity.sql`

Counts how many developers have worked with each database tool. Databases are split from the multi-value `DatabaseHaveWorkedWith` field.

| Column            | Description                       |
| ----------------- | --------------------------------- |
| `database_tools`  | Name of the database or tool      |
| `developer_count` | Number of respondents who used it |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- dbt installed and configured

### Step 1 — Set up the Python environment

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install pandas dbt-core
```

### Step 2 — Download the raw survey data

The raw survey file is not included in this repository. Download `survey_results_public.csv` from the Stack Overflow Annual Developer Survey page and place it in the **project root** folder (next to `extract.py`).

### Step 3 — Extract the sample data

Run the Python script to generate the seed file from the raw survey:

```bash
python extract.py
```

This reads `survey_results_public.csv` and writes a 5,000-row random sample to `seeds/raw_survey.csv`.

### Step 4 — Load the seed into the database

```bash
dbt seed
```

### Step 5 — Run the models

```bash
dbt run
```

This builds both the staging view and all three marts tables.

### Step 6 — Run data tests

```bash
dbt test
```

---

## ⚙️ Configuration

The dbt project profile is named `stackoverflow_survey`.

Model materialization defaults:

| Layer     | Type  |
| --------- | ----- |
| `staging` | View  |
| `marts`   | Table |

---

## 📌 Notes

- The `survey_results_public.csv` raw file is not committed to the repository (it is listed in `.gitignore`). You need to download it separately from the Stack Overflow survey website and place it in the project root before running `extract.py`.
- The seed file `raw_survey.csv` contains only 5,000 randomly sampled rows (using `random_state=42` for reproducibility).
