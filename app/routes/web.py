from flask import Blueprint, render_template

web_bp = Blueprint("web", __name__)


@web_bp.get("/")
def dashboard():
    return render_template("dashboard.html")
