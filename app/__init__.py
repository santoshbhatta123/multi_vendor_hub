from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_migrate import Migrate
from config.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    import pymysql
    try:
        conn = pymysql.connect(host='localhost', user='root', password='')
        conn.cursor().execute('CREATE DATABASE IF NOT EXISTS multi_vendor_hub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        conn.close()
    except Exception:
        pass

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.blueprints.auth.routes import auth
    from app.blueprints.admin.routes import admin
    from app.blueprints.vendor.routes import vendor
    from app.blueprints.customer.routes import customer
    from app.blueprints.payment.routes import payment_bp

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(vendor, url_prefix='/vendor')
    app.register_blueprint(customer, url_prefix='/')
    app.register_blueprint(payment_bp)

    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)

    with app.app_context():
        from app.models import user, vendor as vendor_model, customer as customer_model, product, category, subcategory, cart, order, payment, review
        db.create_all()

        import os
        for folder in ['vendor_images', 'avatars', 'category_images']:
            os.makedirs(os.path.join(app.root_path, 'static', folder), exist_ok=True)

        from app.models.category import Category
        from app.models.subcategory import SubCategory
        from app.models.vendor import Vendor
        from app.models.customer import Customer
        from app.models.user import User

        if not Category.query.first():
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
                db.session.add(Category(name=name, slug=slug, description=desc, is_active=True))
            db.session.commit()

            cat_map = {c.slug: c for c in Category.query.all()}
            for slug, name, cat_slug in [
                ('mobile-phones', 'Mobile Phones', 'electronics'),
                ('laptops', 'Laptops', 'electronics'),
                ('headphones', 'Headphones', 'electronics'),
                ('men-fashion', 'Men Fashion', 'clothing'),
                ('women-fashion', 'Women Fashion', 'clothing'),
                ('footwear', 'Footwear', 'clothing'),
                ('furniture', 'Furniture', 'home-garden'),
                ('decor', 'Decor', 'home-garden'),
                ('fiction', 'Fiction', 'books'),
                ('non-fiction', 'Non-Fiction', 'books'),
            ]:
                db.session.add(SubCategory(category_id=cat_map[cat_slug].id, name=name, slug=slug, is_active=True))
            db.session.commit()

        if not User.query.filter_by(role='admin').first():
            admin = User(username='admin', email='admin@multivendorhub.com', role='admin', is_active=True, email_verified=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

        if not User.query.filter_by(role='vendor').first():
            v = User(username='vendor1', email='vendor@example.com', role='vendor', is_active=True, email_verified=True)
            v.set_password('vendor123')
            db.session.add(v)
            db.session.flush()
            db.session.add(Vendor(user_id=v.id, store_name='Demo Store', store_slug='demo-store', is_approved=True, is_verified=True))
            db.session.commit()

        if not User.query.filter_by(role='customer').first():
            c = User(username='customer1', email='customer@example.com', role='customer', is_active=True, email_verified=True)
            c.set_password('customer123')
            db.session.add(c)
            db.session.flush()
            db.session.add(Customer(user_id=c.id, full_name='John Doe'))
            db.session.commit()

    return app
