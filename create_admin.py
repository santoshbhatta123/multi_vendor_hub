from run import app
from app import db, bcrypt
from app.models.user import User
from app.models.vendor import Vendor
from app.models.customer import Customer
from app.models.category import Category
from app.models.subcategory import SubCategory

with app.app_context():
    db.create_all()

    if User.query.filter_by(role='admin').first():
        print("Admin already exists.")
    else:
        admin = User(username='admin', email='admin@multivendorhub.com', role='admin', is_active=True, email_verified=True)
        admin.set_password('admin123')
        db.session.add(admin)

        for name, slug, desc in [
            ('Electronics', 'electronics', 'Electronic devices'),
            ('Clothing', 'clothing', 'Fashion and apparel'),
            ('Home & Garden', 'home-garden', 'Home improvement'),
            ('Books', 'books', 'Books'),
            ('Sports', 'sports', 'Sports equipment'),
            ('Health & Beauty', 'health-beauty', 'Health products'),
            ('Toys', 'toys', 'Toys and games'),
            ('Automotive', 'automotive', 'Car accessories'),
        ]:
            if not Category.query.filter_by(slug=slug).first():
                db.session.add(Category(name=name, slug=slug, description=desc, is_active=True))

        db.session.commit()

        cats = {c.slug: c for c in Category.query.all()}

        sub_data = [
            ('mobile-phones', 'Mobile Phones', cats['electronics']),
            ('laptops', 'Laptops', cats['electronics']),
            ('headphones', 'Headphones', cats['electronics']),
            ('men-fashion', 'Men Fashion', cats['clothing']),
            ('women-fashion', 'Women Fashion', cats['clothing']),
            ('footwear', 'Footwear', cats['clothing']),
            ('furniture', 'Furniture', cats['home-garden']),
            ('decor', 'Decor', cats['home-garden']),
            ('fiction', 'Fiction', cats['books']),
            ('non-fiction', 'Non-Fiction', cats['books']),
        ]
        for slug, name, cat in sub_data:
            if not SubCategory.query.filter_by(slug=slug, category_id=cat.id).first():
                db.session.add(SubCategory(category_id=cat.id, name=name, slug=slug, is_active=True))

        db.session.commit()
        print("Admin, categories, and subcategories created!")

    if not User.query.filter_by(role='vendor').first():
        vuser = User(username='vendor1', email='vendor@example.com', role='vendor', is_active=True, email_verified=True)
        vuser.set_password('vendor123')
        db.session.add(vuser)
        db.session.flush()
        db.session.add(Vendor(user_id=vuser.id, store_name='Demo Store', store_slug='demo-store', is_approved=True, is_verified=True))
        db.session.commit()
        print("Vendor account created!")

    if not User.query.filter_by(role='customer').first():
        cuser = User(username='customer1', email='customer@example.com', role='customer', is_active=True, email_verified=True)
        cuser.set_password('customer123')
        db.session.add(cuser)
        db.session.flush()
        db.session.add(Customer(user_id=cuser.id, full_name='John Doe'))
        db.session.commit()
        print("Customer account created!")

    print("\nDefault logins:")
    print("  Admin:    admin@multivendorhub.com / admin123")
    print("  Vendor:   vendor@example.com / vendor123")
    print("  Customer: customer@example.com / customer123")
