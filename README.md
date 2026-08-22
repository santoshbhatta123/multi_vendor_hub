# Multi Vendor Hub

A complete multi-vendor e-commerce platform built with Python Flask and Bootstrap 5. This project allows multiple vendors to register and sell their products, while customers can browse, shop, and make payments through eSewa.

## Features

### Authentication System
- Multi-role login/registration (Admin, Vendor, Customer)
- Secure password hashing with Flask-Bcrypt
- Session management with Flask-Login
- Forgot/Reset password
- Email validation
- Role-based access control

### Vendor Features
- Vendor dashboard with analytics
- Store profile management
- Product CRUD with image upload
- Product categories and stock management
- Order management with status updates
- Sales analytics and earnings tracking

### Customer Features
- Browse and search products
- Filter by category, price, and rating
- Shopping cart management
- Wishlist functionality
- Checkout with eSewa payment
- Order history and tracking
- Product reviews and ratings

### Admin Features
- Admin dashboard with statistics
- Vendor management (approve/suspend)
- Customer management
- Product approval workflow
- Category management
- Order management
- Sales reports and analytics
- Review moderation

### Payment Integration
- eSewa wallet payment gateway
- Payment verification and validation
- Transaction history

## Tech Stack

- **Backend:** Python Flask 3.0
- **Database:** MySQL with SQLAlchemy ORM
- **Frontend:** Bootstrap 5, jQuery
- **Authentication:** Flask-Login, Flask-Bcrypt
- **Forms:** Flask-WTF, WTForms
- **Payment:** eSewa API
- **Image Processing:** Pillow

## Project Structure

```
multi_vendor_hub/
├── run.py                      # Application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── config/
│   ├── __init__.py
│   └── config.py               # Application configuration
├── database/
│   └── schema.sql              # Database schema
├── app/
│   ├── __init__.py             # App factory
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── vendor.py
│   │   ├── customer.py
│   │   ├── product.py
│   │   ├── category.py
│   │   ├── cart.py
│   │   ├── order.py
│   │   ├── payment.py
│   │   └── review.py
│   ├── forms/                  # WTForms
│   │   ├── __init__.py
│   │   ├── auth_forms.py
│   │   ├── admin_forms.py
│   │   ├── vendor_forms.py
│   │   └── customer_forms.py
│   ├── blueprints/             # Route blueprints
│   │   ├── auth/__init__.py & routes.py
│   │   ├── admin/__init__.py & routes.py
│   │   ├── vendor/__init__.py & routes.py
│   │   └── customer/__init__.py & routes.py
│   ├── utils/                  # Utility functions
│   │   ├── __init__.py
│   │   ├── decorators.py
│   │   ├── helpers.py
│   │   └── error_handlers.py
│   ├── templates/              # Jinja2 templates
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── admin/
│   │   ├── vendor/
│   │   ├── customer/
│   │   ├── errors/
│   │   └── emails/
│   └── static/                 # Static assets
│       ├── css/style.css
│       ├── js/main.js
│       ├── images/
│       └── vendor_images/
└── migrations/                 # Flask-Migrate
```

## Installation Guide

### Prerequisites
- Python 3.8+
- MySQL 5.7+ or MariaDB 10+
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd multi_vendor_hub
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup MySQL Database
1. Start your MySQL server
2. Login to MySQL:
```bash
mysql -u root -p
```
3. Run the schema file:
```sql
source database/schema.sql
```

### Step 5: Configure Application
Edit `config/config.py` and update:
- `SECRET_KEY`: Change to a secure random key
- `SQLALCHEMY_DATABASE_URI`: Update your MySQL credentials
- `MAIL_*`: Configure email settings
- `ESEWA_*`: Update eSewa merchant credentials

### Step 6: Run the Application
```bash
python run.py
```

### Step 7: Access the Application
- Website: http://localhost:5000
- Admin Panel: http://localhost:5000/admin/dashboard

### Default Admin Credentials
- Email: admin@multivendorhub.com
- Password: admin123

## User Roles

### Admin
- Full access to manage vendors, customers, products, orders
- Dashboard with analytics and reports
- Product approval workflow
- Review moderation

### Vendor/Seller
- Register as a vendor
- Manage store profile
- Add/edit/delete products
- View orders and update status
- Track earnings

### Customer/Buyer
- Browse and search products
- Add items to cart and wishlist
- Place orders with eSewa payment
- Write product reviews

## eSewa Integration

To integrate eSewa payment:
1. Register for eSewa merchant account at https://esewa.com.np
2. Update `ESEWA_MERCHANT_ID` and `ESEWA_SECRET_KEY` in `config/config.py`
3. For testing, use eSewa's test environment URLs

## Security Features
- CSRF protection (Flask-WTF)
- SQL injection prevention (SQLAlchemy ORM)
- Password hashing (Flask-Bcrypt)
- Session security (Flask-Login)
- Input validation (WTForms)
- Role-based access decorators
- File upload validation
