from app import db
from datetime import datetime


class SubCategory(db.Model):
    __tablename__ = 'subcategories'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    category = db.relationship('Category', backref='subcategories', lazy=True)
    products = db.relationship('Product', backref='subcategory', lazy=True)

    __table_args__ = (
        db.UniqueConstraint('category_id', 'slug', name='uq_category_subcategory_slug'),
    )

    def __repr__(self):
        return f"SubCategory('{self.name}')"
