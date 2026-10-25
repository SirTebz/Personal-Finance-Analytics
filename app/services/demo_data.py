"""Synthetic records for a safe, immediately useful portfolio demonstration."""
from datetime import date
from decimal import Decimal
import random

from app.extensions import db
from app.models.category import Category
from app.models.transaction import Transaction


EXPENSES = {
    "Housing": 8500,
    "Groceries": 2200,
    "Transport": 1400,
    "Utilities": 1200,
    "Entertainment": 650,
    "Healthcare": 450,
    "Subscriptions": 280,
    "Shopping": 900,
}


def seed_demo_data():
    """Seed one reproducible year only when the database has no transactions."""
    if Transaction.query.count():
        return False
    categories = {
        name: Category(name=name, transaction_type=transaction_type)
        for transaction_type, names in (("Income", ["Salary", "Freelance"]), ("Expense", list(EXPENSES)))
        for name in names
    }
    db.session.add_all(categories.values())
    db.session.flush()
    random.seed(26)
    for month in range(1, 13):
        db.session.add(Transaction(category_id=categories["Salary"].id, transaction_date=date(2026, month, 25), transaction_type="Income", description="Monthly salary", amount=Decimal("28500"), payment_method="Bank Transfer"))
        if month in (3, 6, 9, 12):
            db.session.add(Transaction(category_id=categories["Freelance"].id, transaction_date=date(2026, month, 14), transaction_type="Income", description="Freelance project", amount=Decimal(str(random.randrange(2800, 7200))), payment_method="Bank Transfer"))
        for category, base in EXPENSES.items():
            db.session.add(Transaction(category_id=categories[category].id, transaction_date=date(2026, month, random.randint(1, 24)), transaction_type="Expense", description=f"{category} expense", amount=Decimal(str(round(base * random.uniform(.78, 1.22), 2))), payment_method=random.choice(["Card", "EFT", "Cash"])))
    db.session.commit()
    return True
