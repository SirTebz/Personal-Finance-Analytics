import csv
import io

from app.models.category import Category
from app.services.validation import validate_transaction


REQUIRED_COLUMNS = {"date", "type", "description", "amount", "category", "payment_method", "notes"}


def parse_csv(uploaded_file):
    if not uploaded_file or not uploaded_file.filename.lower().endswith(".csv"):
        return None, [{"row": 0, "reason": "Upload a CSV file."}]
    try:
        text = uploaded_file.stream.read().decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(text))
        if not reader.fieldnames or not REQUIRED_COLUMNS.issubset(reader.fieldnames):
            missing = ", ".join(sorted(REQUIRED_COLUMNS - set(reader.fieldnames or [])))
            return None, [{"row": 0, "reason": f"Missing required columns: {missing}"}]
        return list(reader), []
    except UnicodeDecodeError:
        return None, [{"row": 0, "reason": "CSV must be UTF-8 encoded."}]


def validate_csv_rows(rows):
    valid, rejected = [], []
    seen = set()
    categories = {(category.name.casefold(), category.transaction_type): category for category in Category.query.filter_by(is_active=True).all()}
    for index, row in enumerate(rows, start=2):
        transaction_type = row.get("type", "").strip().title()
        category = categories.get((row.get("category", "").strip().casefold(), transaction_type))
        payload = {"transaction_date": row.get("date"), "transaction_type": transaction_type, "description": row.get("description"), "amount": row.get("amount"), "category_id": category.id if category else None, "payment_method": row.get("payment_method"), "notes": row.get("notes")}
        cleaned, errors = validate_transaction(payload, category)
        fingerprint = tuple(payload[key] for key in ("transaction_date", "transaction_type", "description", "amount", "category_id"))
        if fingerprint in seen:
            errors["row"] = "Duplicate row in uploaded file."
        seen.add(fingerprint)
        if errors:
            rejected.append({"row": index, "reason": "; ".join(errors.values())})
        else:
            valid.append(cleaned)
    return valid, rejected
