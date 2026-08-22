from app import db
from datetime import datetime


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True, default='Nepal')
    shipping_address = db.Column(db.Text, nullable=True)
    avatar = db.Column(db.String(255), nullable=True, default='default_avatar.png')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    cart_items = db.relationship('Cart', backref='customer', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='customer', lazy=True)
    reviews = db.relationship('Review', backref='customer', lazy=True)
    wishlist = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"Customer('{self.full_name}')"
