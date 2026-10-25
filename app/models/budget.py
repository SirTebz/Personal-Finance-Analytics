from datetime import datetime, timezone

from app.extensions import db


class Budget(db.Model):
    __tablename__ = "budgets"
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False, index=True)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Numeric(18, 2), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    category = db.relationship("Category", backref=db.backref("budgets", lazy=True))
    __table_args__ = (db.CheckConstraint("month BETWEEN 1 AND 12", name="ck_budget_month"), db.CheckConstraint("amount >= 0", name="ck_budget_amount"), db.UniqueConstraint("category_id", "month", "year", name="uq_budget_category_period"))
