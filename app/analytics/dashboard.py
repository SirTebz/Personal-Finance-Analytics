from collections import defaultdict
from datetime import date
from decimal import Decimal

from sqlalchemy import func

from app.extensions import db
from app.models.category import Category
from app.models.transaction import Transaction


ZERO = Decimal("0.00")


def parse_date_range(args):
    start = args.get("start_date")
    end = args.get("end_date")
    try:
        return (date.fromisoformat(start) if start else None, date.fromisoformat(end) if end else None), None
    except ValueError:
        return (None, None), "Dates must use YYYY-MM-DD."


def filtered_transactions(start_date=None, end_date=None):
    query = Transaction.query.filter_by(is_deleted=False)
    if start_date:
        query = query.filter(Transaction.transaction_date >= start_date)
    if end_date:
        query = query.filter(Transaction.transaction_date <= end_date)
    return query


def money(value):
    return Decimal(value or 0).quantize(Decimal("0.01"))


def dashboard_data(start_date=None, end_date=None):
    query = filtered_transactions(start_date, end_date)
    income = money(query.filter(Transaction.transaction_type == "Income").with_entities(func.sum(Transaction.amount)).scalar())
    expenses = money(query.filter(Transaction.transaction_type == "Expense").with_entities(func.sum(Transaction.amount)).scalar())
    net_cash_flow = income - expenses
    transaction_count = query.count()
    months = {transaction.transaction_date.strftime("%Y-%m") for transaction in query.with_entities(Transaction.transaction_date).all()}
    month_count = max(len(months), 1)

    category_rows = (query.join(Category).filter(Transaction.transaction_type == "Expense")
        .with_entities(Category.name, func.sum(Transaction.amount).label("amount"))
        .group_by(Category.name).order_by(func.sum(Transaction.amount).desc()).all())
    categories = [{"name": name, "amount": float(money(amount)), "percentage": round(float(money(amount) / expenses * 100), 2) if expenses else 0} for name, amount in category_rows]
    largest = query.filter(Transaction.transaction_type == "Expense").order_by(Transaction.amount.desc()).first()

    monthly = defaultdict(lambda: {"income": ZERO, "expenses": ZERO})
    for transaction in query.order_by(Transaction.transaction_date).all():
        key = transaction.transaction_date.strftime("%Y-%m")
        if transaction.transaction_type == "Income":
            monthly[key]["income"] += transaction.amount
        else:
            monthly[key]["expenses"] += transaction.amount
    monthly_data = [{"month": key, "income": float(values["income"]), "expenses": float(values["expenses"]), "net_cash_flow": float(values["income"] - values["expenses"])} for key, values in sorted(monthly.items())]

    return {"summary": {"total_income": float(income), "total_expenses": float(expenses), "net_cash_flow": float(net_cash_flow), "savings_rate": round(float(net_cash_flow / income * 100), 2) if income else 0, "average_monthly_income": float(income / month_count), "average_monthly_expenses": float(expenses / month_count), "highest_spending_category": categories[0]["name"] if categories else None, "largest_transaction": {"description": largest.description, "amount": float(largest.amount), "date": largest.transaction_date.isoformat()} if largest else None, "transaction_count": transaction_count}, "monthly": monthly_data, "categories": categories, "top_expenses": [{"date": transaction.transaction_date.isoformat(), "description": transaction.description, "category": transaction.category.name, "amount": float(transaction.amount)} for transaction in query.filter(Transaction.transaction_type == "Expense").order_by(Transaction.amount.desc()).limit(5).all()]}
