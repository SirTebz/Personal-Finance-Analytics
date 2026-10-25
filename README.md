# Personal Finance Analytics

A Flask-based personal finance analytics portfolio project for recording transactions, analysing spending, and communicating practical financial insights. The app uses SQLAlchemy with SQLite for immediate local development and supports SQL Server through `DATABASE_URL` for the intended production database.

## Current status

The application supports categories, transactions, date-filtered dashboard KPIs and charts, budgets, and validated CSV import/export. The included seed script creates only synthetic demo data.

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Open `http://127.0.0.1:5000`.

Copy `.env.example` to `.env` and set `DATABASE_URL` to connect to SQL Server. Without it, the app creates a local SQLite database in the Flask instance directory.

## Test

```powershell
pytest
```

## Demo data

Run `python scripts/generate_sample_data.py` once after setup. It generates 12 months of 2026 synthetic data in your configured database.

## Portfolio analysis

`database/schema.sql` and `database/queries/financial_analysis.sql` provide SQL Server reference assets. The notebooks show data cleaning, exploratory analysis, and reproducible insights using an exported CSV. See `docs/` for the architecture, data dictionary, and calculation definitions.

## Limitations

This is a local portfolio application with synthetic data. It has no bank integration, investment tracking, tax calculations, financial advice, or forecasting.

## Render deployment

This repository includes `render.yaml` for a free Flask web service. In Render, create the service from this GitHub repository, then set `SECRET_KEY` to a long, private random value. Leave `DATABASE_URL` blank for a temporary SQLite portfolio demo. SQLite storage on a free Render web service is ephemeral, so data may reset when the service restarts or deploys.

Set `SEED_DEMO_DATA=true` on Render to automatically create the synthetic 2026 demo dataset whenever its database starts empty. The setting is safe to leave enabled: it never adds demo records to a database that already has transactions.
