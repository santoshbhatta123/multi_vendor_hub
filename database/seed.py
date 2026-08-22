from app import create_app, db, bcrypt
from app.models.user import User
from app.models.vendor import Vendor
from app.models.customer import Customer
from app.models.category import Category
from app.models.subcategory import SubCategory
from app.models.product import Product
import random

app = create_app()

with app.app_context():
    db.create_all()

    if User.query.first():
        print("Database already has data. Skipping seed.")
        exit()

    admin = User(
        username='admin',
        email='admin@multivendorhub.com',
        role='admin',
        is_active=True,
        email_verified=True
    )
    admin.set_password('admin123')
    db.session.add(admin)

    categories_data = [
        ('Electronics', 'electronics', 'Electronic devices and accessories'),
        ('Clothing', 'clothing', 'Fashion and apparel'),
        ('Home & Garden', 'home-garden', 'Home improvement and garden supplies'),
        ('Books', 'books', 'Books and educational materials'),
        ('Sports', 'sports', 'Sports equipment and accessories'),
        ('Health & Beauty', 'health-beauty', 'Health and beauty products'),
        ('Toys', 'toys', 'Toys and games'),
        ('Automotive', 'automotive', 'Car and automotive accessories'),
    ]

    categories = []
    for name, slug, desc in categories_data:
        cat = Category(name=name, slug=slug, description=desc, is_active=True)
        db.session.add(cat)
        categories.append(cat)

    db.session.commit()

    vendors_data = [
        ('tech_store', 'techstore@example.com', 'TechStore', 'tech-store', 'Best electronics'),
        ('fashion_hub', 'fashion@example.com', 'FashionHub', 'fashion-hub', 'Trendy clothing'),
        ('home_decor', 'home@example.com', 'HomeDecor', 'home-decor', 'Beautiful home items'),
        ('bookworm', 'books@example.com', 'BookWorm', 'book-worm', 'All kinds of books'),
    ]

    vendors = []
    for uname, email, store, slug, desc in vendors_data:
        user = User(username=uname, email=email, role='vendor', is_active=True, email_verified=True)
        user.set_password('vendor123')
        db.session.add(user)
        db.session.flush()

        vendor = Vendor(
            user_id=user.id,
            store_name=store,
            store_slug=slug,
            store_description=desc,
            is_approved=True,
            is_verified=True,
            city='Kathmandu',
            country='Nepal',
            phone='98' + str(random.randint(10000000, 99999999))
        )
        db.session.add(vendor)
        vendors.append(vendor)

    customer_user = User(
        username='customer1',
        email='customer@example.com',
        role='customer',
        is_active=True,
        email_verified=True
    )
    customer_user.set_password('customer123')
    db.session.add(customer_user)
    db.session.flush()

    customer = Customer(
        user_id=customer_user.id,
        full_name='John Doe',
        phone='9812345678',
        address='Kathmandu, Nepal',
        city='Kathmandu',
        shipping_address='Kathmandu, Nepal'
    )
    db.session.add(customer)

    db.session.commit()

    subcategories_data = {
        categories[0]: ['Mobile Phones', 'Laptops', 'Headphones', 'Cameras'],
        categories[1]: ['Men Fashion', 'Women Fashion', 'Kids Fashion', 'Footwear'],
        categories[2]: ['Furniture', 'Decor', 'Kitchen'],
        categories[3]: ['Fiction', 'Non-Fiction', 'Educational'],
        categories[4]: ['Fitness', 'Outdoor'],
    }

    subcategories = {}
    for cat, subs in subcategories_data.items():
        subcategories[cat] = []
        for sub_name in subs:
            sub = SubCategory(
                category_id=cat.id,
                name=sub_name,
                slug=sub_name.lower().replace(' ', '-'),
                is_active=True
            )
            db.session.add(sub)
            subcategories[cat].append(sub)

    db.session.commit()

    product_templates = [
        ('Smartphone XYZ', 'Latest smartphone with great features', 25000, 22000, 50, categories[0], vendors[0], 0),
        ('Laptop Pro', 'High-performance laptop', 85000, 79999, 30, categories[0], vendors[0], 1),
        ('Wireless Headphones', 'Noise-cancelling headphones', 3500, 2999, 100, categories[0], vendors[0], 2),
        ('Smart Watch', 'Fitness tracking smartwatch', 8000, 6499, 75, categories[0], vendors[0], None),
        ('USB-C Hub', '7-in-1 USB-C hub adapter', 1500, None, 200, categories[0], vendors[0], None),

        ('Men Casual Shirt', 'Comfortable cotton shirt', 1500, 1199, 80, categories[1], vendors[1], 4),
        ('Women Dress', 'Elegant evening dress', 3500, 2799, 40, categories[1], vendors[1], 5),
        ('Denim Jacket', 'Classic denim jacket', 4500, 3799, 60, categories[1], vendors[1], 4),
        ('Sports Shoes', 'Comfortable running shoes', 5500, 4499, 90, categories[1], vendors[1], 7),

        ('Table Lamp', 'Modern LED table lamp', 2500, 1999, 50, categories[2], vendors[2], 9),
        ('Wall Art', 'Beautiful canvas wall art', 1800, 1499, 35, categories[2], vendors[2], 9),
        ('Cushion Set', 'Decorative cushion set of 4', 2200, 1799, 45, categories[2], vendors[2], 9),

        ('Python Programming', 'Learn Python from scratch', 800, 649, 150, categories[3], vendors[3], 13),
        ('Data Science Guide', 'Complete data science handbook', 1200, 999, 100, categories[3], vendors[3], 13),
        ('Fiction Novel', 'Bestselling fiction novel', 600, 499, 200, categories[3], vendors[3], 11),
        ('Cookbook', '500 healthy recipes', 900, 749, 80, categories[3], vendors[3], None),
    ]

    for name, desc, price, disc_price, stock, cat, ven, sub_idx in product_templates:
        sub_id = subcategories[cat][sub_idx].id if sub_idx is not None and sub_idx < len(subcategories[cat]) else None
        product = Product(
            vendor_id=ven.id,
            category_id=cat.id,
            sub_category_id=sub_id,
            name=name,
            slug=name.lower().replace(' ', '-') + '-' + str(random.randint(1000, 9999)),
            description=desc,
            price=price,
            discounted_price=disc_price,
            stock=stock,
            is_active=True,
            is_approved=True,
            status='approved',
            average_rating=round(random.uniform(3.0, 5.0), 1),
            review_count=random.randint(0, 20),
            sold_count=random.randint(5, 100),
            is_featured=random.choice([True, False])
        )
        db.session.add(product)

    db.session.commit()
    print("Database seeded successfully!")
    print("\nDefault Logins:")
    print("  Admin:    admin@multivendorhub.com / admin123")
    print("  Vendor:   techstore@example.com / vendor123")
    print("  Customer: customer@example.com / customer123")
