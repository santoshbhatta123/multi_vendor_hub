from app import db
from datetime import datetime


class Vendor(db.Model):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    store_name = db.Column(db.String(100), nullable=False)
    store_slug = db.Column(db.String(100), unique=True, nullable=False)
    store_description = db.Column(db.Text, nullable=True)
    store_logo = db.Column(db.String(255), nullable=True, default='default_store.png')
    store_banner = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True, default='Nepal')
    is_verified = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)
    commission_rate = db.Column(db.Float, default=10.0)
    total_earnings = db.Column(db.Float, default=0.0)
    available_balance = db.Column(db.Float, default=0.0)
    total_sales = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    products = db.relationship('Product', backref='vendor', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='vendor', lazy=True)

    def __repr__(self):
        return f"Vendor('{self.store_name}')"
