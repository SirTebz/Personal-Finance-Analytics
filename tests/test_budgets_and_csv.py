import io
from datetime import date
from decimal import Decimal

from app.extensions import db
from app.models.category import Category
from app.models.transaction import Transaction


def test_budget_compares_actual_spending(client, app):
    with app.app_context():
        category = Category(name="Transport", transaction_type="Expense")
        db.session.add(category)
        db.session.flush()
        db.session.add(Transaction(category_id=category.id, transaction_date=date(2026, 10, 5), transaction_type="Expense", description="Fuel", amount=Decimal("650")))
        db.session.commit()
        category_id = category.id
    response = client.post("/api/budgets", json={"category_id": category_id, "month": 10, "year": 2026, "amount": "2000"})
    assert response.status_code == 201
    budget = client.get("/api/budgets?month=10&year=2026").json["data"][0]
    assert budget["actual"] == 650.0
    assert budget["remaining"] == 1350.0
    assert budget["percentage_used"] == 32.5
    updated = client.put(f"/api/budgets/{budget['id']}", json={"amount": "2500"})
    assert updated.status_code == 200
    assert updated.json["data"]["amount"] == 2500.0
    assert client.delete(f"/api/budgets/{budget['id']}").status_code == 204


def test_csv_import_reports_invalid_rows_and_exports(client):
    category = client.post("/api/categories", json={"name": "Dining", "transaction_type": "Expense"}).json["data"]
    content = "date,type,description,amount,category,payment_method,notes\n2026-10-02,Expense,Lunch,125.50,Dining,Card,ok\ninvalid,Expense,Bad,-2,Dining,Card,no\n"
    response = client.post("/api/import/csv", data={"file": (io.BytesIO(content.encode()), "transactions.csv")}, content_type="multipart/form-data")
    assert response.status_code == 200
    assert response.json["imported"] == 1
    assert response.json["rejected"] == 1
    export = client.get("/api/export/csv?type=Expense")
    assert export.status_code == 200
    assert b"Lunch" in export.data
    assert category["name"].encode() in export.data
