from datetime import date

from flask import Blueprint, jsonify, request
from sqlalchemy import or_

from app.extensions import db
from app.models.category import Category
from app.models.transaction import Transaction
from app.services.validation import VALID_TRANSACTION_TYPES, validate_transaction

api_bp = Blueprint("api", __name__)


@api_bp.get("/health")
def health():
    return jsonify({"status": "ok"})


def category_payload(category):
    return {"id": category.id, "name": category.name, "transaction_type": category.transaction_type, "description": category.description, "is_active": category.is_active}


def transaction_payload(transaction):
    return {"id": transaction.id, "category_id": transaction.category_id, "category": transaction.category.name, "transaction_date": transaction.transaction_date.isoformat(), "transaction_type": transaction.transaction_type, "description": transaction.description, "amount": f"{transaction.amount:.2f}", "payment_method": transaction.payment_method, "notes": transaction.notes}


@api_bp.get("/categories")
def list_categories():
    query = Category.query.order_by(Category.transaction_type, Category.name)
    if request.args.get("active") == "true":
        query = query.filter_by(is_active=True)
    return jsonify({"data": [category_payload(category) for category in query.all()]})


@api_bp.post("/categories")
def create_category():
    payload = request.get_json(silent=True) or {}
    name = str(payload.get("name", "")).strip()
    transaction_type = payload.get("transaction_type")
    if not name or transaction_type not in VALID_TRANSACTION_TYPES:
        return jsonify({"error": "Provide a category name and valid transaction type."}), 400
    if Category.query.filter_by(name=name).first():
        return jsonify({"error": "A category with this name already exists."}), 409
    category = Category(name=name, transaction_type=transaction_type, description=str(payload.get("description", "")).strip() or None)
    db.session.add(category)
    db.session.commit()
    return jsonify({"data": category_payload(category)}), 201


@api_bp.get("/transactions")
def list_transactions():
    query = Transaction.query.filter_by(is_deleted=False).join(Category)
    if request.args.get("type") in VALID_TRANSACTION_TYPES:
        query = query.filter(Transaction.transaction_type == request.args["type"])
    if request.args.get("category_id", type=int):
        query = query.filter(Transaction.category_id == request.args.get("category_id", type=int))
    if request.args.get("start_date"):
        query = query.filter(Transaction.transaction_date >= date.fromisoformat(request.args["start_date"]))
    if request.args.get("end_date"):
        query = query.filter(Transaction.transaction_date <= date.fromisoformat(request.args["end_date"]))
    if request.args.get("min_amount", type=float) is not None:
        query = query.filter(Transaction.amount >= request.args.get("min_amount", type=float))
    if request.args.get("max_amount", type=float) is not None:
        query = query.filter(Transaction.amount <= request.args.get("max_amount", type=float))
    if search := request.args.get("search", "").strip():
        term = f"%{search}%"
        query = query.filter(or_(Transaction.description.ilike(term), Transaction.payment_method.ilike(term), Category.name.ilike(term)))
    results = query.order_by(Transaction.transaction_date.desc(), Transaction.id.desc()).all()
    return jsonify({"data": [transaction_payload(transaction) for transaction in results]})


@api_bp.post("/transactions")
def create_transaction():
    cleaned, errors = validate_transaction(request.get_json(silent=True) or {})
    if errors:
        return jsonify({"errors": errors}), 400
    transaction = Transaction(category_id=cleaned["category"].id, transaction_date=cleaned["transaction_date"], transaction_type=cleaned["transaction_type"], description=cleaned["description"], amount=cleaned["amount"], payment_method=cleaned["payment_method"], notes=cleaned["notes"])
    db.session.add(transaction)
    db.session.commit()
    return jsonify({"data": transaction_payload(transaction)}), 201


@api_bp.get("/transactions/<int:transaction_id>")
def get_transaction(transaction_id):
    transaction = db.session.get(Transaction, transaction_id)
    if transaction is None or transaction.is_deleted:
        return jsonify({"error": "Transaction not found."}), 404
    return jsonify({"data": transaction_payload(transaction)})


@api_bp.put("/transactions/<int:transaction_id>")
def update_transaction(transaction_id):
    transaction = db.session.get(Transaction, transaction_id)
    if transaction is None or transaction.is_deleted:
        return jsonify({"error": "Transaction not found."}), 404
    cleaned, errors = validate_transaction(request.get_json(silent=True) or {})
    if errors:
        return jsonify({"errors": errors}), 400
    for attribute in ("transaction_date", "transaction_type", "description", "amount", "payment_method", "notes"):
        setattr(transaction, attribute, cleaned[attribute])
    transaction.category_id = cleaned["category"].id
    db.session.commit()
    return jsonify({"data": transaction_payload(transaction)})


@api_bp.delete("/transactions/<int:transaction_id>")
def delete_transaction(transaction_id):
    transaction = db.session.get(Transaction, transaction_id)
    if transaction is None or transaction.is_deleted:
        return jsonify({"error": "Transaction not found."}), 404
    transaction.is_deleted = True
    db.session.commit()
    return "", 204
