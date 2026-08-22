# Multi Vendor Hub — Project Report

---

## Cover Page

**Project Title:** Multi Vendor Hub — Multi-Vendor E-Commerce Platform  
**Course:** [Your Course Name]  
**Department:** [Your Department]  
**Submitted By:** [Your Name]  
**Roll No:** [Your Roll No]  
**Supervisor:** [Supervisor Name]  
**Date:** July 2026  

---

## Certificate

This is to certify that the project entitled **"Multi Vendor Hub — Multi-Vendor E-Commerce Platform"** is a bonafide work carried out in partial fulfillment of the requirements for the degree of [Your Degree] at [Your Institution].

**Supervisor:** _______________  
**Head of Department:** _______________  
**External Examiner:** _______________  

---

## Abstract

Multi Vendor Hub is a web-based multi-vendor e-commerce platform built using Python Flask framework with MySQL database backend. The platform enables multiple vendors to register, manage their product catalogs, and sell products to customers through a unified marketplace. Key features include role-based authentication (Admin, Vendor, Customer), product management with hierarchical categories and subcategories, shopping cart with AJAX-powered dynamic subcategory loading, and integrated eSewa V2 digital wallet payment processing using HMAC-SHA256 signature verification. The frontend is built with Bootstrap 5 for responsive design. The system follows the Waterfall development methodology and has been tested across all user roles. The eSewa payment integration uses the official V2 API with proper signature generation, server-side verification, and error handling for secure transaction processing.

**Keywords:** Multi-vendor, e-commerce, Flask, eSewa, HMAC-SHA256, SQLAlchemy, Bootstrap 5

---

## Table of Contents
1. Introduction
2. Literature Review & System Analysis
3. System Design
4. Implementation
5. Testing & Results
6. Conclusion & Future Work
References

---

# Chapter 1: Introduction

## 1.1 Background
The rapid growth of internet penetration in Nepal has created significant opportunities for online commerce. However, small and medium-sized vendors face barriers in establishing their online presence due to the complexity and cost of existing e-commerce solutions. Multi-vendor marketplaces provide a shared platform where multiple sellers can offer their products to a wide customer base, reducing individual overhead costs.

## 1.2 Problem Statement
Current e-commerce solutions in Nepal either lack support for local payment methods like eSewa, are prohibitively expensive for small vendors, or require significant technical expertise to set up and maintain. There is a need for an affordable, user-friendly multi-vendor platform with integrated local digital payment support.

## 1.3 Objectives
1. Design and develop a multi-vendor e-commerce platform with role-based access control
2. Implement product management with category-subcategory hierarchy
3. Integrate eSewa V2 payment gateway for secure online transactions
4. Build a responsive, user-friendly interface using Bootstrap 5
5. Provide comprehensive admin, vendor, and customer dashboards

## 1.4 Scope of the Project
The platform supports three user roles: Admin (platform management), Vendor (product and order management), and Customer (browsing, cart, checkout). The eSewa V2 API integration handles payment initiation, signature verification, and transaction status checking. The system is designed for deployment on local or cloud servers with MySQL database.

## 1.5 Organization of the Report
This report is organized into five chapters. Chapter 1 introduces the project. Chapter 2 covers literature review and system analysis. Chapter 3 presents system design including architecture and database design. Chapter 4 describes implementation details. Chapter 5 covers testing and results, followed by conclusions.

---

# Chapter 2: Literature Review & System Analysis

## 2.1 Existing Systems
Several multi-vendor platforms exist globally including Shopify, WooCommerce, and Magento. In Nepal, platforms like Sastodeal and Daraz operate as multi-vendor marketplaces. However, these are large-scale proprietary solutions not suitable for small vendors.

## 2.2 eSewa Payment Gateway
eSewa is Nepal's leading digital wallet with over 8 million users [1]. The eSewa ePay V2 API provides merchants with a secure payment processing system using HMAC-SHA256 signatures for request authentication and response verification [2]. The API supports both sandbox (testing) and production environments.

## 2.3 Flask Framework
Flask is a lightweight Python web framework that follows the WSGI standard. It provides routing, templating (Jinja2), session management, and extensibility through blueprints and extensions [3]. Flask-SQLAlchemy provides ORM integration for database operations.

## 2.4 System Requirements

### Functional Requirements
- User registration and authentication with role-based access
- Product CRUD operations for vendors
- Category and subcategory management
- Shopping cart with quantity management
- Checkout with shipping details
- eSewa V2 payment processing
- Order tracking and status management
- Customer reviews and ratings
- Wishlist functionality

### Non-Functional Requirements
- Responsive design for mobile and desktop
- Secure password hashing (bcrypt)
- CSRF protection on all forms
- Session-based authentication
- Database transaction integrity

## 2.5 Feasibility Study
The project is technically feasible using Flask, MySQL, and the eSewa V2 API. Economically, all technologies are open-source with zero licensing cost. Operationally, the system requires only a web server and MySQL database.

---

# Chapter 3: System Design

## 3.1 Architecture
The system follows a **3-tier architecture**:
1. **Presentation Layer:** HTML5, CSS3 (Bootstrap 5), JavaScript, Jinja2 templates
2. **Application Layer:** Python Flask with blueprints for modular design
3. **Data Layer:** MySQL with SQLAlchemy ORM

### Blueprint Structure
| Blueprint | URL Prefix | Purpose |
|-----------|-----------|---------|
| auth | /auth | Login, Register, Logout |
| admin | /admin | Platform administration |
| vendor | /vendor | Vendor dashboard and product management |
| customer | / | Product browsing, cart, checkout |
| payment | / | eSewa V2 payment processing |

## 3.2 Database Design

### Entity Relationship Diagram (ERD)

```
User (1) ──── (1) Customer ──── (N) Cart ──── (N) Product
User (1) ──── (1) Vendor ──── (N) Product
User (1) ──── (1) Admin
Category (1) ──── (N) SubCategory ──── (N) Product
Customer (1) ──── (N) Order ──── (N) OrderItem ──── (N) Product
Order (1) ──── (1) Payment
Customer (1) ──── (N) Review ──── (1) Product
Customer (1) ──── (N) Wishlist
```

### Key Tables

**Users Table**
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment ID |
| email | VARCHAR(120) UNIQUE | Login email |
| password | VARCHAR(200) | Bcrypt hashed password |
| role | VARCHAR(20) | admin/vendor/customer |

**Orders Table**
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment ID |
| order_number | VARCHAR(50) UNIQUE | Generated order number |
| customer_id | FK → customers.id | Customer reference |
| vendor_id | FK → vendors.id | Vendor reference |
| total_amount | FLOAT | Order total in NPR |
| status | VARCHAR(20) | pending/processing/delivered |
| payment_status | VARCHAR(20) | unpaid/paid/failed |
| transaction_uuid | VARCHAR(255) | eSewa transaction UUID |

**Payments Table**
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment ID |
| order_id | FK → orders.id | Order reference |
| transaction_id | VARCHAR(255) UNIQUE | eSewa transaction ID |
| merchant_code | VARCHAR(50) | EPAYTEST / production code |
| amount | FLOAT | Payment amount |
| status | VARCHAR(50) | pending/success/failed |
| ref_id | VARCHAR(255) | eSewa reference ID |
| oid | VARCHAR(255) UNIQUE | eSewa order ID |
| response_data | JSON | Full eSewa response |

## 3.3 Payment Flow (eSewa V2)

```
Customer → Checkout → Server generates HMAC-SHA256 signature
    → Form POST to eSewa V2 URL (rc-epay.esewa.com.np)
    → Customer logs in with eSewa credentials
    → eSewa processes payment
    → Redirect to success_url with data (base64-encoded)
    → Server decodes data, verifies HMAC signature
    → Server calls eSewa status API for final verification
    → Payment recorded in database
    → Order status updated to confirmed
```

## 3.4 Security Measures
- **Password Hashing:** bcrypt with salt rounds
- **CSRF Protection:** Flask-WTF CSRF tokens on all forms
- **Payment Signature:** HMAC-SHA256 with `key=value` message format
- **Server-Side Verification:** eSewa status API call after callback
- **Role-Based Access:** Custom decorators (@admin_required, @vendor_required, @customer_required)

---

# Chapter 4: Implementation

## 4.1 Project Structure
```
multi_vendor_hub/
├── run.py                      # Entry point
├── config/config.py            # Configuration
├── app/
│   ├── __init__.py             # App factory + auto-seed
│   ├── blueprints/
│   │   ├── auth/routes.py      # Authentication
│   │   ├── admin/routes.py     # Admin panel
│   │   ├── vendor/routes.py    # Vendor dashboard
│   │   ├── customer/routes.py  # Customer features
│   │   └── payment/routes.py   # eSewa V2 integration
│   ├── models/                  # SQLAlchemy models
│   ├── forms/                   # WTForms
│   ├── templates/               # Jinja2 templates
│   ├── static/                  # CSS, JS, images
│   └── utils/                   # Helpers, decorators
└── docs/                        # Documentation
```

## 4.2 eSewa V2 Signature Generation
```python
message = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
signature = base64.b64encode(
    hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()
).decode()
```
The signature uses the `key=value` format with base64 encoding as per the official eSewa V2 specification [2].

## 4.3 Payment Verification
```python
# Decode base64 response from eSewa
decoded = base64.b64decode(encoded_data).decode()
data = json.loads(decoded)

# Recompute signature and compare
expected_signature = base64.b64encode(
    hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()
).decode()

if signature == expected_signature:
    # Additional verification via eSewa status API
    response = requests.get(status_url, params={...})
```

## 4.4 Key Features Implemented
1. **Auto-Database Creation:** App creates MySQL database if not exists
2. **Auto-Seeding:** Default categories, subcategories, and user accounts seeded on first run
3. **AJAX Subcategory Loading:** Dynamic subcategory dropdown based on selected category
4. **Cart Management:** Add, update, remove items with stock validation
5. **Multi-Vendor Orders:** Cart items grouped by vendor for separate order creation
6. **Vendor Dashboard:** Sales analytics, product management, order tracking
7. **Customer Features:** Wishlist, reviews, order history, profile management

## 4.5 Default Accounts
| Role | Email | Password |
|------|-------|----------|
| Admin | admin@multivendorhub.com | admin123 |
| Vendor | vendor@example.com | vendor123 |
| Customer | customer@example.com | customer123 |

---

# Chapter 5: Testing & Results

## 5.1 Testing Strategy
- **Unit Testing:** Individual function testing for models and utilities
- **Integration Testing:** Blueprint route testing with Flask test client
- **User Acceptance Testing:** Manual testing of all user workflows

## 5.2 Test Cases

| Test Case | Input | Expected Result | Actual Result | Status |
|-----------|-------|----------------|---------------|--------|
| User Registration | Valid details | Account created | Account created | Pass |
| Login | Correct credentials | Redirect to dashboard | Redirect to dashboard | Pass |
| Add to Cart | Product + quantity | Cart updated | Cart updated | Pass |
| Checkout | Shipping details + eSewa | Order created | Order created | Pass |
| eSewa Payment | Valid credentials | Payment processed | Payment processed | Pass |
| Vendor Add Product | Product details | Product listed | Product listed | Pass |
| Admin Manage Users | User action | User updated | User updated | Pass |

## 5.3 Results
The platform successfully handles multi-vendor product management, shopping cart operations, and eSewa V2 payment processing. The responsive Bootstrap 5 interface works across desktop and mobile devices. The auto-seeding feature ensures the system is ready for use immediately after deployment.

---

# Conclusion & Future Work

## Conclusion
Multi Vendor Hub is a fully functional multi-vendor e-commerce platform built with Flask and integrated with eSewa V2 payment gateway. The platform provides role-based access control, comprehensive product management, and secure payment processing. The use of HMAC-SHA256 signatures ensures transaction integrity, while the modular blueprint architecture allows for easy extension and maintenance.

## Future Work
1. **Mobile App:** Develop React Native or Flutter mobile application
2. **Real-Time Notifications:** Implement WebSocket-based order status notifications
3. **Advanced Analytics:** Add sales analytics dashboard with charts and reports
4. **Multi-Payment Support:** Integrate Khalti, IME Pay, and credit/debit card payments
5. **Search Optimization:** Implement Elasticsearch for product search
6. **Deployment:** Deploy to cloud platforms (AWS, DigitalOcean) with Docker

---

## References

[1] eSewa Digital Wallet. "eSewa — Nepal's Leading Digital Wallet." https://www.esewa.com.np/

[2] eSewa Developer Documentation. "ePay V2 API Integration." https://developer.esewa.com.np/pages/Epay-V2

[3] Flask Documentation. "Flask — Python Web Framework." https://flask.palletsprojects.com/

[4] SQLAlchemy. "SQLAlchemy ORM Documentation." https://docs.sqlalchemy.org/

[5] Bootstrap. "Bootstrap 5 — CSS Framework." https://getbootstrap.com/

[6] Flask-Login. "User Session Management." https://flask-login.readthedocs.io/

[7] OWASP Foundation. "OWASP Top Ten Web Application Security Risks." https://owasp.org/www-project-top-ten/

[8] RFC 2104. "HMAC: Keyed-Hashing for Message Authentication." https://tools.ietf.org/html/rfc2104
