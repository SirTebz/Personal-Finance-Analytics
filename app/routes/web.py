from flask import Blueprint, render_template

web_bp = Blueprint("web", __name__)


@web_bp.get("/")
def dashboard():
    return render_template("dashboard.html")


@web_bp.get("/transactions")
def transactions():
    return render_template("transactions.html")


@web_bp.get("/budgets")
def budgets():
    return render_template("budgets.html")


@web_bp.get("/import")
def import_data():
    return render_template("import.html")


@web_bp.get("/categories")
def categories():
    return render_template("categories.html")
