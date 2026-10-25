import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask

from app.extensions import db


def create_app(test_config=None):
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    default_database = f"sqlite:///{Path(app.instance_path) / 'personal_finance.sqlite3'}"
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "development-only-change-me"),
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL") or default_database,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        MAX_CONTENT_LENGTH=5 * 1024 * 1024,
    )
    if test_config:
        app.config.update(test_config)
    db.init_app(app)
    from app.routes.web import web_bp
    from app.routes.api import api_bp
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    with app.app_context():
        from app import models  # noqa: F401
        db.create_all()
    return app
