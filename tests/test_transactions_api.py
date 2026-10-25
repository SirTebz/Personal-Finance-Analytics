def create_category(client, name="Groceries", transaction_type="Expense"):
    response = client.post("/api/categories", json={"name": name, "transaction_type": transaction_type})
    assert response.status_code == 201
    return response.json["data"]


def transaction_data(category_id, **overrides):
    data = {"transaction_date": "2026-10-10", "transaction_type": "Expense", "description": "Weekly groceries", "amount": "450.50", "category_id": category_id, "payment_method": "Card", "notes": "Demo"}
    data.update(overrides)
    return data


def test_create_filter_update_and_soft_delete_transaction(client):
    category = create_category(client)
    created = client.post("/api/transactions", json=transaction_data(category["id"]))
    assert created.status_code == 201
    transaction_id = created.json["data"]["id"]
    assert created.json["data"]["amount"] == "450.50"

    listing = client.get("/api/transactions", query_string={"search": "groceries"})
    assert len(listing.json["data"]) == 1

    updated = client.put(f"/api/transactions/{transaction_id}", json=transaction_data(category["id"], amount="500", description="Monthly groceries"))
    assert updated.status_code == 200
    assert updated.json["data"]["amount"] == "500.00"

    assert client.delete(f"/api/transactions/{transaction_id}").status_code == 204
    assert client.get(f"/api/transactions/{transaction_id}").status_code == 404
    assert client.get("/api/transactions").json["data"] == []


def test_transaction_rejects_invalid_amount_and_mismatched_category(client):
    income_category = create_category(client, "Salary", "Income")
    response = client.post("/api/transactions", json=transaction_data(income_category["id"], amount="-1"))
    assert response.status_code == 400
    assert "amount" in response.json["errors"]
    assert "category_id" in response.json["errors"]


def test_categories_require_unique_name(client):
    create_category(client)
    duplicate = client.post("/api/categories", json={"name": "Groceries", "transaction_type": "Expense"})
    assert duplicate.status_code == 409


def test_category_update_and_safe_deactivation(client):
    category = create_category(client)
    updated = client.put(f"/api/categories/{category['id']}", json={"name": "Food", "transaction_type": "Expense", "is_active": True})
    assert updated.status_code == 200
    assert updated.json["data"]["name"] == "Food"
