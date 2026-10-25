from datetime import date
from decimal import Decimal

from app.extensions import db
from app.models.category import Category
from app.models.transaction import Transaction


def test_dashboard_calculates_financial_kpis(client, app):
    with app.app_context():
        salary = Category(name="Salary", transaction_type="Income")
        food = Category(name="Groceries", transaction_type="Expense")
        db.session.add_all([salary, food])
        db.session.flush()
        db.session.add_all([
            Transaction(category_id=salary.id, transaction_date=date(2026, 1, 10), transaction_type="Income", description="Salary", amount=Decimal("25000")),
            Transaction(category_id=food.id, transaction_date=date(2026, 1, 11), transaction_type="Expense", description="Food", amount=Decimal("7500")),
            Transaction(category_id=food.id, transaction_date=date(2026, 2, 11), transaction_type="Expense", description="Food 2", amount=Decimal("10000")),
        ])
        db.session.commit()
    response = client.get("/api/dashboard?start_date=2026-01-01&end_date=2026-12-31")
    assert response.status_code == 200
    summary = response.json["data"]["summary"]
    assert summary["total_income"] == 25000.0
    assert summary["total_expenses"] == 17500.0
    assert summary["net_cash_flow"] == 7500.0
    assert summary["savings_rate"] == 30.0
    assert summary["highest_spending_category"] == "Groceries"


def test_dashboard_rejects_invalid_dates(client):
    response = client.get("/api/dashboard?start_date=not-a-date")
    assert response.status_code == 400
