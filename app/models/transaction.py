from datetime import datetime, timezone

from app.extensions import db


class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False, index=True)
    transaction_date = db.Column(db.Date, nullable=False, index=True)
    transaction_type = db.Column(db.String(10), nullable=False, index=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Numeric(18, 2), nullable=False)
    payment_method = db.Column(db.String(60), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    category = db.relationship("Category", backref=db.backref("transactions", lazy=True))
    __table_args__ = (db.CheckConstraint("transaction_type IN ('Income', 'Expense')", name="ck_transaction_type"), db.CheckConstraint("amount > 0", name="ck_transaction_amount"))
