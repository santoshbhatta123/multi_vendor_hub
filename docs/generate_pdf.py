# -*- coding: utf-8 -*-
import os
from fpdf import FPDF

OUTPUT_DIR = r"C:\multi_vendor_hub\docs"


class ReportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "I", 9)
        self.cell(0, 8, "Multi Vendor Hub", align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 9)
        self.cell(0, 10, "Page %d" % self.page_no(), align="C")

    def chapter_title(self, title):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def section_title(self, title):
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def sub_section(self, title):
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text):
        self.set_font("Helvetica", "", 11)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def bullet(self, text):
        self.set_font("Helvetica", "", 11)
        self.set_x(self.l_margin)
        self.multi_cell(0, 6, "  - " + text)


def generate_report():
    pdf = ReportPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # =============================================
    # Chapter 1: Introduction
    # =============================================
    pdf.add_page()
    pdf.chapter_title("Chapter 1: Introduction")

    pdf.section_title("1.1 Introduction")
    pdf.body_text(
        "The rapid growth of internet penetration in Nepal has created significant "
        "opportunities for online commerce. Small and medium-sized vendors face "
        "barriers in establishing their online presence due to the complexity and "
        "cost of existing e-commerce solutions. Multi-vendor marketplaces provide a "
        "shared platform where multiple sellers can offer their products to a wide "
        "customer base, reducing individual overhead costs."
    )
    pdf.body_text(
        "Multi Vendor Hub is a web-based multi-vendor e-commerce platform built "
        "using Python Flask framework with MySQL database backend. The platform "
        "enables multiple vendors to register, manage their product catalogs, and "
        "sell products to customers through a unified marketplace. It integrates "
        "eSewa V2 digital wallet for online payment processing using HMAC-SHA256 "
        "signature verification. The frontend is built with Bootstrap 5 for "
        "responsive design."
    )

    pdf.section_title("1.2 Problem Statement")
    pdf.body_text(
        "Current e-commerce solutions in Nepal either lack support for local payment "
        "methods like eSewa, are prohibitively expensive for small vendors, or "
        "require significant technical expertise to set up and maintain. Existing "
        "platforms like Daraz and Sastodeal are large-scale proprietary solutions "
        "not suitable for individual small vendors who want their own online store "
        "within a marketplace."
    )
    pdf.body_text(
        "There is a need for an affordable, user-friendly multi-vendor platform "
        "with integrated local digital payment support that allows vendors to "
        "manage their products and orders independently while sharing a common "
        "customer base and payment infrastructure."
    )

    pdf.section_title("1.3 Objectives")
    pdf.bullet("Design and develop a multi-vendor e-commerce platform with role-based access control (Admin, Vendor, Customer)")
    pdf.bullet("Implement product management with hierarchical category and subcategory system")
    pdf.bullet("Integrate eSewa V2 payment gateway for secure online transactions using HMAC-SHA256")
    pdf.bullet("Build a responsive, user-friendly interface using Bootstrap 5")
    pdf.bullet("Provide comprehensive admin, vendor, and customer dashboards")
    pdf.bullet("Implement shopping cart, checkout, order tracking, and review system")
    pdf.bullet("Ensure secure authentication and authorization using Flask-Login and bcrypt")
    pdf.ln(3)

    pdf.section_title("1.4 Scope and Limitations")
    pdf.sub_section("Scope")
    pdf.body_text(
        "The platform supports three user roles: Admin (platform management), "
        "Vendor (product and order management), and Customer (browsing, cart, "
        "checkout). The eSewa V2 API integration handles payment initiation, "
        "HMAC-SHA256 signature verification, and transaction status checking. "
        "The system supports category-subcategory-product hierarchy, shopping "
        "cart with stock validation, multi-vendor order splitting, customer "
        "reviews, and wishlist functionality."
    )
    pdf.sub_section("Limitations")
    pdf.bullet("eSewa sandbox accounts are managed by eSewa and may be deactivated")
    pdf.bullet("No real-time notification system for order status updates")
    pdf.bullet("No mobile application (web only)")
    pdf.bullet("No integrated shipping/tracking system")
    pdf.bullet("Payment limited to eSewa digital wallet only")
    pdf.ln(3)

    pdf.section_title("1.5 Report Organization")
    pdf.body_text(
        "This report is organized into five chapters. Chapter 1 introduces the "
        "project with problem statement, objectives, and scope. Chapter 2 covers "
        "background study and literature review. Chapter 3 presents system analysis "
        "and design including requirements, feasibility, data modelling, and "
        "architectural design. Chapter 4 describes implementation details and "
        "testing. Chapter 5 concludes with lessons learned and future recommendations."
    )

    # =============================================
    # Chapter 2: Background Study and Literature Review
    # =============================================
    pdf.add_page()
    pdf.chapter_title("Chapter 2: Background Study and Literature Review")

    pdf.section_title("2.1 Background Study")
    pdf.sub_section("2.1.1 Flask Framework")
    pdf.body_text(
        "Flask is a lightweight Python web framework that follows the WSGI "
        "(Web Server Gateway Interface) standard. It was created by Armin "
        "Ronacher as part of the Pocoo project. Flask provides routing, "
        "templating (Jinja2), session management, cookie handling, and "
        "extensibility through blueprints and extensions [3]."
    )
    pdf.body_text(
        "Key Flask extensions used in this project: Flask-SQLAlchemy (ORM "
        "integration), Flask-Login (user session management), Flask-Bcrypt "
        "(password hashing), Flask-WTF (form handling with CSRF protection), "
        "Flask-Mail (email sending), and Flask-Migrate (database migrations)."
    )

    pdf.sub_section("2.1.2 SQLAlchemy ORM")
    pdf.body_text(
        "SQLAlchemy is a Python SQL toolkit and Object-Relational Mapping (ORM) "
        "library. It provides a full suite of enterprise-level persistence "
        "patterns. SQLAlchemy ORM allows Python classes to be mapped to "
        "database tables, enabling developers to interact with the database "
        "using Python objects instead of raw SQL queries [4]."
    )

    pdf.sub_section("2.1.3 eSewa ePay V2 API")
    pdf.body_text(
        "eSewa is Nepal's leading digital wallet with over 8 million users. "
        "The eSewa ePay V2 API provides merchants with a secure payment "
        "processing system. The V2 API uses HMAC-SHA256 signatures for request "
        "authentication. The signature message format is: "
        "total_amount={amount},transaction_uuid={uuid},product_code={code}, "
        "encoded using base64 [2]."
    )
    pdf.body_text(
        "Payment flow: (1) Merchant generates HMAC-SHA256 signature, "
        "(2) Customer is redirected to eSewa with signed form data, "
        "(3) Customer logs in and confirms payment, "
        "(4) eSewa redirects to success_url with base64-encoded response, "
        "(5) Merchant verifies signature and records payment."
    )

    pdf.sub_section("2.1.4 Bootstrap 5")
    pdf.body_text(
        "Bootstrap is a free and open-source CSS framework directed at "
        "responsive, mobile-first front-end web development. Bootstrap 5 "
        "provides CSS classes for layout, typography, forms, buttons, tables, "
        "and JavaScript components like modals, dropdowns, and carousels [5]."
    )

    pdf.sub_section("2.1.5 Role-Based Access Control")
    pdf.body_text(
        "Role-Based Access Control (RBAC) is a method of restricting system "
        "access based on the roles of individual users. In this project, "
        "three roles are defined: Admin (full platform access), Vendor "
        "(product and order management), and Customer (browsing, purchasing). "
        "Access is enforced using Flask-Login decorators and custom decorators "
        "(@admin_required, @vendor_required, @customer_required)."
    )

    pdf.section_title("2.2 Literature Review")
    pdf.body_text(
        "Several multi-vendor e-commerce platforms exist globally. Shopify "
        "offers a hosted multi-vendor solution but requires monthly subscription "
        "fees. WooCommerce with Dokan plugin provides open-source multi-vendor "
        "capabilities but requires WordPress. Magento supports multi-vendor "
        "marketplaces but has high server requirements."
    )
    pdf.body_text(
        "In Nepal, Daraz and Sastodeal operate as multi-vendor marketplaces "
        "but are proprietary platforms. The eSewa developer documentation [2] "
        "provides comprehensive API integration guides. Studies on e-commerce "
        "in Nepal highlight the need for local payment integration and "
        "affordable solutions for small vendors."
    )
    pdf.body_text(
        "This project addresses these gaps by providing an open-source, "
        "Flask-based multi-vendor platform with native eSewa V2 integration, "
        "auto-database creation, auto-seeding of default data, and a "
        "lightweight architecture suitable for small to medium deployments."
    )

    # =============================================
    # Chapter 3: System Analysis and Design
    # =============================================
    pdf.add_page()
    pdf.chapter_title("Chapter 3: System Analysis and Design")

    pdf.section_title("3.1 System Analysis")

    pdf.sub_section("3.1.1 Requirement Analysis")
    pdf.body_text("Functional Requirements:")
    pdf.bullet("User registration and login with role-based access (Admin, Vendor, Customer)")
    pdf.bullet("Admin: Manage users, vendors, categories, subcategories, and view platform statistics")
    pdf.bullet("Vendor: Add, edit, delete products; view orders; manage store profile; view sales analytics")
    pdf.bullet("Customer: Browse products by category/subcategory; add to cart; checkout with eSewa; view order history; write reviews; manage wishlist")
    pdf.bullet("Product management with name, description, price, discount price, stock, images")
    pdf.bullet("Category and subcategory hierarchy with AJAX dynamic loading")
    pdf.bullet("Shopping cart with add, update quantity, remove, and stock validation")
    pdf.bullet("Checkout with shipping address and phone number collection")
    pdf.bullet("eSewa V2 payment processing with HMAC-SHA256 signature and server-side verification")
    pdf.bullet("Order creation with multi-vendor splitting (separate orders per vendor)")
    pdf.bullet("Order status tracking (pending, processing, shipped, delivered, cancelled)")
    pdf.bullet("Customer reviews and ratings for products")
    pdf.bullet("Auto-database creation and auto-seeding of default categories and users")
    pdf.ln(3)

    pdf.body_text("Non-Functional Requirements:")
    pdf.bullet("Responsive design for desktop and mobile using Bootstrap 5")
    pdf.bullet("Secure password hashing using bcrypt with salt rounds")
    pdf.bullet("CSRF protection on all forms using Flask-WTF")
    pdf.bullet("Session-based authentication using Flask-Login")
    pdf.bullet("Database transaction integrity with SQLAlchemy")
    pdf.bullet("Proper error handling with user-friendly flash messages")
    pdf.ln(3)

    pdf.sub_section("3.1.2 Feasibility Analysis")
    pdf.sub_section("Technical Feasibility")
    pdf.body_text(
        "The project uses Python Flask (open-source), MySQL (free), Bootstrap 5 "
        "(free), and eSewa sandbox API (free for development). All technologies "
        "are well-documented with active communities. The development team has "
        "access to all required tools and resources."
    )
    pdf.sub_section("Operational Feasibility")
    pdf.body_text(
        "The platform is designed for easy operation. Vendors can manage products "
        "through an intuitive dashboard. Customers can browse and purchase using "
        "familiar web interfaces. Admin can manage the platform through a "
        "centralized dashboard. eSewa is widely used in Nepal, making payment "
        "operations familiar to users."
    )
    pdf.sub_section("Economic Feasibility")
    pdf.body_text(
        "All technologies are open-source with zero licensing costs. The project "
        "requires only a web server and MySQL database, which can run on "
        "affordable hosting. The development cost is minimal as it uses "
        "existing frameworks and libraries."
    )
    pdf.sub_section("Schedule Feasibility")
    pdf.body_text(
        "The project follows the Waterfall methodology and can be completed "
        "within the academic semester timeframe. Each phase has clear "
        "deliverables and milestones."
    )

    pdf.sub_section("3.1.3 Data Modelling (ER Diagram)")
    pdf.body_text(
        "The Entity-Relationship model consists of the following entities "
        "and relationships:"
    )
    pdf.body_text(
        "User (id, email, password, role) -- 1:1 --> Customer (user_id, full_name, "
        "address, phone, shipping_address, wishlist)\n"
        "User -- 1:1 --> Vendor (user_id, store_name, store_description, image)\n"
        "User -- 1:1 --> Admin (user_id,)\n"
        "Category (id, name, description) -- 1:N --> SubCategory (id, category_id, name)\n"
        "SubCategory -- 1:N --> Product (id, vendor_id, category_id, subcategory_id, name, "
        "description, price, discount_price, stock, image)\n"
        "Customer -- 1:N --> Cart (id, customer_id, product_id, quantity)\n"
        "Customer -- 1:N --> Order (id, order_number, customer_id, vendor_id, total_amount, "
        "status, payment_status, transaction_uuid, shipping_address, phone)\n"
        "Order -- 1:N --> OrderItem (id, order_id, product_id, product_name, quantity, price, total)\n"
        "Order -- 1:1 --> Payment (id, order_id, transaction_id, merchant_code, amount, "
        "status, ref_id, oid, response_data)\n"
        "Customer -- 1:N --> Review (id, customer_id, product_id, rating, comment)\n"
        "Customer -- 1:N --> Wishlist (id, customer_id, product_id)"
    )

    pdf.sub_section("3.1.4 Process Modelling (DFD)")
    pdf.body_text(
        "Level 0 DFD (Context Diagram):\n"
        "External Entities: Customer, Vendor, Admin, eSewa Payment Gateway\n"
        "Processes: Multi Vendor Hub System\n"
        "Data Flows:\n"
        "  Customer --> Register/Login, Browse Products, Add to Cart, Checkout, Pay via eSewa\n"
        "  Vendor --> Register/Manage Products, View Orders, Update Order Status\n"
        "  Admin --> Manage Users, Manage Categories, View Reports\n"
        "  eSewa --> Payment Request, Payment Response, Transaction Verification"
    )
    pdf.body_text(
        "Level 1 DFD:\n"
        "1.0 User Authentication: Register, Login, Role Management\n"
        "2.0 Product Management: Add/Edit/Delete Products, Category Management\n"
        "3.0 Shopping: Browse, Search, Cart, Wishlist\n"
        "4.0 Order Processing: Checkout, Order Creation, Multi-Vendor Splitting\n"
        "5.0 Payment Processing: eSewa V2 Form, Signature Generation, Callback Verification\n"
        "6.0 Order Management: Status Tracking, Delivery, Cancellation\n"
        "7.0 Review System: Submit Review, Rating Calculation"
    )

    pdf.section_title("3.2 System Design")

    pdf.sub_section("3.2.1 Architectural Design")
    pdf.body_text(
        "The system follows a 3-tier architecture:\n\n"
        "Presentation Layer: HTML5, CSS3 (Bootstrap 5), JavaScript, jQuery, "
        "Jinja2 templates. Handles user interface and client-side interactions.\n\n"
        "Application Layer: Python Flask with modular blueprint architecture. "
        "Each blueprint handles a specific domain: auth, admin, vendor, customer, "
        "payment. Uses Flask-Login for session management, Flask-WTF for form "
        "validation, and custom decorators for role-based access control.\n\n"
        "Data Layer: MySQL database with SQLAlchemy ORM. Handles data persistence, "
        "relationships, and transactions. Auto-creates database and seeds default "
        "data on first run."
    )
    pdf.body_text(
        "Blueprint Structure:\n"
        "  auth (/auth): Login, Register, Logout\n"
        "  admin (/admin): User management, Category management, Dashboard\n"
        "  vendor (/vendor): Product CRUD, Order management, Analytics\n"
        "  customer (/): Browse, Cart, Checkout, Orders, Reviews, Wishlist\n"
        "  payment (/): eSewa V2 pay, success callback, failure callback"
    )

    pdf.sub_section("3.2.2 Database Schema Design")
    pdf.body_text(
        "Users Table: id (INT PK), email (VARCHAR UNIQUE), password (VARCHAR), "
        "role (VARCHAR: admin/vendor/customer)\n\n"
        "Customers Table: id (INT PK), user_id (FK->users), full_name (VARCHAR), "
        "address (TEXT), phone (VARCHAR), shipping_address (TEXT), wishlist (JSON)\n\n"
        "Vendors Table: id (INT PK), user_id (FK->users), store_name (VARCHAR), "
        "store_description (TEXT), image (VARCHAR)\n\n"
        "Categories Table: id (INT PK), name (VARCHAR), description (TEXT)\n\n"
        "SubCategories Table: id (INT PK), category_id (FK->categories), name (VARCHAR)\n\n"
        "Products Table: id (INT PK), vendor_id (FK->vendors), category_id (FK), "
        "subcategory_id (FK), name (VARCHAR), description (TEXT), price (FLOAT), "
        "discount_price (FLOAT), stock (INT), image (VARCHAR)\n\n"
        "Orders Table: id (INT PK), order_number (VARCHAR UNIQUE), customer_id (FK), "
        "vendor_id (FK), total_amount (FLOAT), status (VARCHAR), payment_status (VARCHAR), "
        "transaction_uuid (VARCHAR), shipping_address (TEXT), phone (VARCHAR)\n\n"
        "Payments Table: id (INT PK), order_id (FK), transaction_id (VARCHAR UNIQUE), "
        "merchant_code (VARCHAR), amount (FLOAT), status (VARCHAR), payment_method (VARCHAR), "
        "ref_id (VARCHAR), oid (VARCHAR UNIQUE), response_data (JSON), error_message (VARCHAR)\n\n"
        "OrderItems Table: id (INT PK), order_id (FK), product_id (FK), product_name (VARCHAR), "
        "quantity (INT), price (FLOAT), total (FLOAT)\n\n"
        "Reviews Table: id (INT PK), customer_id (FK), product_id (FK), rating (INT), "
        "comment (TEXT)"
    )

    pdf.sub_section("3.2.3 Interface Design")
    pdf.body_text(
        "The user interface follows Bootstrap 5 responsive design patterns:\n\n"
        "Base Template (base.html): Navigation bar with logo, category dropdown, "
        "search bar, cart icon, user menu. Footer with links and copyright.\n\n"
        "Home Page: Hero banner, featured categories, latest products grid.\n\n"
        "Product Listing: Sidebar with category/subcategory filters, product grid "
        "with image, name, price, add-to-cart button.\n\n"
        "Product Detail: Large image, product info, price, stock status, add-to-cart, "
        "reviews section.\n\n"
        "Checkout: Shipping form, order summary, eSewa payment button.\n\n"
        "Vendor Dashboard: Sidebar navigation, product table, order table, sales stats.\n\n"
        "Admin Dashboard: User management table, category management, platform statistics."
    )

    pdf.sub_section("3.2.4 Physical DFD")
    pdf.body_text(
        "The physical DFD maps processes to specific files and modules:\n\n"
        "1.0 User Authentication --> app/blueprints/auth/routes.py, "
        "app/models/user.py, app/forms/auth_forms.py\n\n"
        "2.0 Product Management --> app/blueprints/vendor/routes.py, "
        "app/models/product.py, app/forms/product_forms.py\n\n"
        "3.0 Shopping --> app/blueprints/customer/routes.py, "
        "app/models/cart.py, app/templates/customer/*.html\n\n"
        "4.0 Order Processing --> app/blueprints/customer/routes.py "
        "(checkout function), app/models/order.py\n\n"
        "5.0 Payment Processing --> app/blueprints/payment/routes.py, "
        "config/config.py (eSewa settings), app/templates/customer/esewa_payment.html\n\n"
        "6.0 Order Management --> app/blueprints/vendor/routes.py "
        "(order management), app/blueprints/customer/routes.py (order detail)\n\n"
        "Data Stores: MySQL database (multi_vendor_hub), "
        "File system (product images in app/static/vendor_images/)"
    )

    # =============================================
    # Chapter 4: Implementation and Testing
    # =============================================
    pdf.add_page()
    pdf.chapter_title("Chapter 4: Implementation and Testing")

    pdf.section_title("4.1 Implementation")

    pdf.sub_section("4.1.1 Tools Used")
    pdf.body_text(
        "Development Tools:\n"
        "  - IDE: Visual Studio Code\n"
        "  - Version Control: Git\n"
        "  - Database: MySQL (XAMPP)\n"
        "  - Package Manager: pip (conda environment: multivendor)\n"
        "  - API Testing: cURL\n\n"
        "Programming Languages:\n"
        "  - Backend: Python 3.10\n"
        "  - Frontend: HTML5, CSS3, JavaScript, jQuery\n"
        "  - Templating: Jinja2\n\n"
        "Frameworks and Libraries:\n"
        "  - Flask 3.x (web framework)\n"
        "  - Flask-SQLAlchemy (ORM)\n"
        "  - Flask-Login (authentication)\n"
        "  - Flask-Bcrypt (password hashing)\n"
        "  - Flask-WTF (forms + CSRF)\n"
        "  - Flask-Mail (email)\n"
        "  - Flask-Migrate (database migrations)\n"
        "  - Bootstrap 5 (CSS framework)\n"
        "  - requests (HTTP client for eSewa API)\n\n"
        "Database Platform:\n"
        "  - MySQL 8.x (via XAMPP)\n"
        "  - PyMySQL (Python MySQL driver)"
    )

    pdf.sub_section("4.1.2 Implementation Details of Modules")
    pdf.sub_section("Authentication Module (app/blueprints/auth/routes.py)")
    pdf.body_text(
        "Registration: Collects email, password, role (vendor/customer). Creates "
        "User record with bcrypt-hashed password. Creates corresponding Customer "
        "or Vendor profile. Logs in user automatically after registration.\n\n"
        "Login: Validates email and password using bcrypt. Stores user session "
        "using Flask-Login. Redirects to appropriate dashboard based on role.\n\n"
        "Logout: Clears user session and redirects to home page."
    )

    pdf.sub_section("Vendor Module (app/blueprints/vendor/routes.py)")
    pdf.body_text(
        "Dashboard: Shows sales statistics (total sales, monthly sales, order "
        "count, product count). Displays recent orders and low-stock products.\n\n"
        "Product CRUD: Add/Edit/Delete products with image upload. Fields: name, "
        "description, category, subcategory, price, discount price, stock. "
        "Subcategory dropdown loads dynamically via AJAX based on selected category.\n\n"
        "Order Management: View orders for vendor's products. Update order status "
        "(pending, processing, shipped, delivered). View order details and customer "
        "information."
    )

    pdf.sub_section("Customer Module (app/blueprints/customer/routes.py)")
    pdf.body_text(
        "Browse: Product listing with category/subcategory filtering. Search by "
        "product name. Pagination with 12 products per page. Product detail page "
        "with reviews.\n\n"
        "Cart: Add products with quantity validation against stock. Update quantity. "
        "Remove items. Cart total calculation with discounted prices.\n\n"
        "Checkout: Shipping address and phone collection. Cart items grouped by "
        "vendor. Creates separate Order per vendor. Creates OrderItems for each "
        "product. Decrements stock. Clears cart. Redirects to payment.\n\n"
        "Orders: Order history with status badges. Order detail with items and "
        "payment info. Cancel pending/processing orders.\n\n"
        "Reviews: Submit rating (1-5) and comment for purchased products.\n\n"
        "Wishlist: Add/remove products from wishlist. View wishlist page."
    )

    pdf.sub_section("Payment Module (app/blueprints/payment/routes.py)")
    pdf.body_text(
        "Payment Initiation (/pay/<order_id>):\n"
        "  1. Fetches order and validates payment status\n"
        "  2. Generates unique transaction UUID using uuid4()\n"
        "  3. Stores UUID in order.transaction_uuid\n"
        "  4. Generates HMAC-SHA256 signature:\n"
        "     message = total_amount={amount},transaction_uuid={uuid},product_code={code}\n"
        "     signature = base64(hmac-sha256(secret_key, message))\n"
        "  5. Renders esewa_payment.html with signed form fields\n"
        "  6. Form auto-submits to eSewa V2 URL\n\n"
        "Success Callback (/payment/success):\n"
        "  1. Handles V2 (base64-encoded data param) and V1 (refId, oid, amt params)\n"
        "  2. Decodes and parses response data\n"
        "  3. Verifies HMAC-SHA256 signature against expected signature\n"
        "  4. Looks up order by transaction_uuid\n"
        "  5. Creates Payment record with merchant_code, ref_id, oid, response_data\n"
        "  6. Updates order.payment_status = 'paid' and order.status = 'confirmed'\n"
        "  7. Full try/except error handling with flash messages\n\n"
        "V1 Verification (verify_esewa_payment):\n"
        "  1. Generates MD5 hash of total+oid+secret\n"
        "  2. Calls eSewa status API for server-side verification\n"
        "  3. Returns True if status == COMPLETE"
    )

    pdf.sub_section("Auto-Database and Seeding (app/__init__.py)")
    pdf.body_text(
        "On application startup, the app factory checks if the MySQL database "
        "exists. If not, it creates it. Then it checks if default data exists. "
        "If not, it seeds: 8 categories (Electronics, Fashion, Home, Beauty, "
        "Sports, Books, Toys, Grocery), 10 subcategories, and 3 default user "
        "accounts (admin, vendor, customer)."
    )

    pdf.section_title("4.2 Testing")

    pdf.sub_section("4.2.1 Unit Testing")
    pdf.body_text(
        "Test Case 1: User Registration\n"
        "  Input: Valid email, password, role\n"
        "  Expected: User created, profile created, session started\n"
        "  Result: PASS\n\n"
        "Test Case 2: User Login\n"
        "  Input: Correct email and password\n"
        "  Expected: Session created, redirect to dashboard\n"
        "  Result: PASS\n\n"
        "Test Case 3: Password Hashing\n"
        "  Input: Plain text password\n"
        "  Expected: Bcrypt hash stored, not plain text\n"
        "  Result: PASS\n\n"
        "Test Case 4: Role-Based Access\n"
        "  Input: Vendor accessing admin URL\n"
        "  Expected: Access denied, redirect to vendor dashboard\n"
        "  Result: PASS\n\n"
        "Test Case 5: Cart Operations\n"
        "  Input: Add product, update quantity, remove item\n"
        "  Expected: Cart totals update correctly\n"
        "  Result: PASS\n\n"
        "Test Case 6: Stock Validation\n"
        "  Input: Add more than available stock\n"
        "  Expected: Error message, quantity limited to stock\n"
        "  Result: PASS\n\n"
        "Test Case 7: eSewa Signature Generation\n"
        "  Input: Known amount, UUID, product code, secret key\n"
        "  Expected: Correct base64 HMAC-SHA256 signature\n"
        "  Result: PASS (verified against eSewa documentation examples)"
    )

    pdf.sub_section("4.2.2 System Testing")
    pdf.body_text(
        "Test Case 1: Complete Purchase Flow\n"
        "  Steps: Login as customer, browse products, add to cart, checkout, "
        "pay with eSewa (demo mode with MPIN 1234)\n"
        "  Expected: Order created, payment recorded, stock decremented, "
        "cart cleared, order visible in history\n"
        "  Result: PASS\n\n"
        "Test Case 2: Multi-Vendor Order Splitting\n"
        "  Steps: Add products from different vendors to cart, checkout\n"
        "  Expected: Separate orders created per vendor, each with correct "
        "items and totals\n"
        "  Result: PASS\n\n"
        "Test Case 3: Vendor Product Management\n"
        "  Steps: Login as vendor, add product with image, edit price, "
        "delete product\n"
        "  Expected: Product appears/disappears from customer browse, "
        "image uploaded correctly\n"
        "  Result: PASS\n\n"
        "Test Case 4: Admin User Management\n"
        "  Steps: Login as admin, view users, delete user\n"
        "  Expected: User list updates, deleted user cannot login\n"
        "  Result: PASS\n\n"
        "Test Case 5: eSewa V2 Payment Integration\n"
        "  Steps: Complete checkout, verify form POSTs to eSewa V2 URL "
        "with correct signature fields\n"
        "  Expected: Valid HMAC-SHA256 signature, correct form fields, "
        "eSewa login page loads\n"
        "  Result: PASS (sandbox login requires active eSewa test accounts)\n\n"
        "Test Case 6: Responsive Design\n"
        "  Steps: Access site on mobile, tablet, desktop viewports\n"
        "  Expected: Layout adapts, navigation works, forms usable\n"
        "  Result: PASS"
    )

    # =============================================
    # Chapter 5: Conclusion and Future Recommendations
    # =============================================
    pdf.add_page()
    pdf.chapter_title("Chapter 5: Conclusion and Future Recommendations")

    pdf.section_title("5.1 Lessons Learned / Outcome")
    pdf.body_text(
        "1. Flask Blueprint Architecture: Modular blueprint design significantly "
        "improves code organization and maintainability. Each feature domain "
        "(auth, vendor, customer, payment) is isolated and independently testable.\n\n"
        "2. eSewa V2 Integration: The HMAC-SHA256 signature generation requires "
        "precise message format (key=value pairs) and base64 encoding. The sandbox "
        "environment may be unreliable, requiring fallback mechanisms.\n\n"
        "3. AJAX Dynamic Loading: Implementing dynamic subcategory loading via AJAX "
        "significantly improves user experience compared to full page reloads.\n\n"
        "4. Database Design: Proper normalization with foreign key relationships "
        "ensures data integrity. Auto-seeding default data simplifies deployment.\n\n"
        "5. Security: CSRF protection, password hashing, and role-based access "
        "control are essential and should be implemented from the start.\n\n"
        "6. Multi-Vendor Logic: Splitting cart items by vendor during checkout "
        "requires careful handling of stock decrements and order creation."
    )

    pdf.section_title("5.2 Conclusion")
    pdf.body_text(
        "Multi Vendor Hub is a fully functional multi-vendor e-commerce platform "
        "built with Python Flask and integrated with eSewa V2 payment gateway. "
        "The platform successfully provides:\n\n"
        "- Role-based access control for Admin, Vendor, and Customer\n"
        "- Complete product management with category-subcategory hierarchy\n"
        "- Shopping cart with stock validation and multi-vendor order splitting\n"
        "- Secure eSewa V2 payment processing with HMAC-SHA256 signatures\n"
        "- Customer reviews, ratings, and wishlist functionality\n"
        "- Responsive Bootstrap 5 interface\n"
        "- Auto-database creation and auto-seeding for easy deployment\n\n"
        "The modular blueprint architecture allows for easy extension and "
        "maintenance. The system is ready for deployment and can serve as a "
        "foundation for a production multi-vendor marketplace."
    )

    pdf.section_title("5.3 Future Recommendations")
    pdf.bullet("Mobile Application: Develop React Native or Flutter mobile apps for Android and iOS platforms")
    pdf.bullet("Multi-Payment Support: Integrate Khalti, IME Pay, and credit/debit card payment gateways alongside eSewa")
    pdf.bullet("Real-Time Notifications: Implement WebSocket-based push notifications for order status updates and messages")
    pdf.bullet("Advanced Search: Integrate Elasticsearch for full-text product search with filters and sorting")
    pdf.bullet("Analytics Dashboard: Add comprehensive sales analytics with charts, graphs, and exportable reports")
    pdf.bullet("Email Notifications: Implement automated order confirmation, shipping updates, and promotional emails")
    pdf.bullet("Coupon System: Add discount coupons, promotional offers, and loyalty programs")
    pdf.bullet("Shipping Integration: Integrate with logistics providers for real-time shipping rates and tracking")
    pdf.bullet("Cloud Deployment: Deploy using Docker containers on AWS, DigitalOcean, or similar cloud platforms")
    pdf.bullet("Performance Optimization: Implement caching (Redis), CDN for static assets, and database query optimization")
    pdf.ln(5)

    pdf.section_title("References")
    pdf.body_text(
        "[1] eSewa Digital Wallet. https://www.esewa.com.np/\n"
        "[2] eSewa Developer Documentation - ePay V2 API.\n"
        "    https://developer.esewa.com.np/pages/Epay-V2\n"
        "[3] Flask Documentation. https://flask.palletsprojects.com/\n"
        "[4] SQLAlchemy ORM Documentation. https://docs.sqlalchemy.org/\n"
        "[5] Bootstrap 5 Documentation. https://getbootstrap.com/\n"
        "[6] Flask-Login Documentation. https://flask-login.readthedocs.io/\n"
        "[7] OWASP Top Ten Web Application Security Risks.\n"
        "    https://owasp.org/www-project-top-ten/\n"
        "[8] RFC 2104 - HMAC: Keyed-Hashing for Message Authentication.\n"
        "    https://tools.ietf.org/html/rfc2104\n"
        "[9] MySQL Documentation. https://dev.mysql.com/doc/\n"
        "[10] Python Documentation. https://docs.python.org/3/"
    )

    path = os.path.join(OUTPUT_DIR, "Multi_Vendor_Hub_Report.pdf")
    pdf.output(path)
    print("Report saved: " + path)


if __name__ == "__main__":
    generate_report()
    print("Done!")
