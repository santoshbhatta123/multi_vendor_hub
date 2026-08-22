from app import db
from datetime import datetime


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    sub_category_id = db.Column(db.Integer, db.ForeignKey('subcategories.id'), nullable=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    discounted_price = db.Column(db.Float, nullable=True)
    stock = db.Column(db.Integer, nullable=False, default=0)
    sku = db.Column(db.String(100), unique=True, nullable=True)
    image_1 = db.Column(db.String(255), nullable=True, default='default_product.png')
    image_2 = db.Column(db.String(255), nullable=True)
    image_3 = db.Column(db.String(255), nullable=True)
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='pending')
    average_rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    sold_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    cart_items = db.relationship('Cart', backref='product', lazy=True)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    reviews = db.relationship('Review', backref='product', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"Product('{self.name}')"
