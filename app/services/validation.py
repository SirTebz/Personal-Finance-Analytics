from datetime import date
from decimal import Decimal, InvalidOperation

from app.extensions import db
from app.models.category import Category


VALID_TRANSACTION_TYPES = {"Income", "Expense"}


def validate_transaction(payload, category=None):
    errors = {}
    required = ("transaction_date", "transaction_type", "description", "amount", "category_id")
    for field in required:
        if payload.get(field) in (None, ""):
            errors[field] = "This field is required."

    transaction_date = None
    if payload.get("transaction_date"):
        try:
            transaction_date = date.fromisoformat(str(payload["transaction_date"]))
        except ValueError:
            errors["transaction_date"] = "Use a valid ISO date (YYYY-MM-DD)."

    transaction_type = payload.get("transaction_type")
    if transaction_type and transaction_type not in VALID_TRANSACTION_TYPES:
        errors["transaction_type"] = "Type must be Income or Expense."

    amount = None
    if payload.get("amount") not in (None, ""):
        try:
            amount = Decimal(str(payload["amount"])).quantize(Decimal("0.01"))
            if amount <= 0:
                errors["amount"] = "Amount must be greater than zero."
        except (InvalidOperation, ValueError):
            errors["amount"] = "Amount must be a valid number."

    if category is None and payload.get("category_id") not in (None, ""):
        category = db.session.get(Category, payload["category_id"])
    if category is None:
        errors["category_id"] = "Choose an existing category."
    elif transaction_type and category.transaction_type != transaction_type:
        errors["category_id"] = "Category type must match transaction type."

    cleaned = {
        "transaction_date": transaction_date,
        "transaction_type": transaction_type,
        "description": str(payload.get("description", "")).strip(),
        "amount": amount,
        "category": category,
        "payment_method": str(payload.get("payment_method", "")).strip() or None,
        "notes": str(payload.get("notes", "")).strip() or None,
    }
    if payload.get("description") and not cleaned["description"]:
        errors["description"] = "Description cannot be blank."
    return cleaned, errors
