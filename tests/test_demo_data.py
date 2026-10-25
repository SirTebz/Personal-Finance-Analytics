from app.extensions import db
from app.models.transaction import Transaction
from app.services.demo_data import seed_demo_data


def test_demo_data_seeds_once(app):
    with app.app_context():
        assert seed_demo_data() is True
        assert Transaction.query.count() >= 100
        assert seed_demo_data() is False
        db.session.rollback()
