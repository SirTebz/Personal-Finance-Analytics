# Personal Finance Analytics

A Flask-based personal finance analytics portfolio project for recording transactions, analysing spending, and communicating practical financial insights. The app uses SQLAlchemy with SQLite for immediate local development and supports SQL Server through `DATABASE_URL` for the intended production database.

## Current status

Phase 1 is complete: the application foundation, configuration, relational models, base dashboard UI, and health endpoint are in place. Transaction management, analytics, budgets, import/export, and portfolio documentation follow in incremental phases.

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
