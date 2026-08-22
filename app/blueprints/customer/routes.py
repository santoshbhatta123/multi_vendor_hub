from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app, abort
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.vendor import Vendor
from app.models.customer import Customer
from app.models.product import Product
from app.models.category import Category
from app.models.subcategory import SubCategory
from app.models.cart import Cart
from app.models.order import Order, OrderItem
from app.models.payment import Payment
from app.models.review import Review
from app.forms.customer_forms import CustomerProfileForm, ReviewForm
from app.utils.decorators import customer_required
from app.utils.helpers import save_image, calculate_cart_total, generate_order_number
from datetime import datetime
from sqlalchemy import func
from urllib.request import urlopen, Request
from urllib.parse import urlencode
import hmac
import hashlib
import base64
import secrets
import uuid
import json
import urllib.request
import urllib.parse

customer = Blueprint('customer', __name__)


@customer.route('/')
def home():
    featured_products = Product.query.filter_by(
        is_featured=True, is_approved=True, is_active=True
    ).order_by(Product.created_at.desc()).limit(8).all()

    new_products = Product.query.filter_by(
        is_approved=True, is_active=True
    ).order_by(Product.created_at.desc()).limit(12).all()

    categories = Category.query.filter_by(is_active=True).all()
    vendors = Vendor.query.filter_by(is_approved=True).limit(6).all()

    return render_template('customer/home.html',
                         featured_products=featured_products,
                         new_products=new_products,
                         categories=categories,
                         vendors=vendors)


@customer.route('/products')
def products():
    page = request.args.get('page', 1, type=int)
    category_slug = request.args.get('category')
    subcategory_slug = request.args.get('subcategory')
    search = request.args.get('search', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort = request.args.get('sort', 'newest')

    query = Product.query.filter_by(is_approved=True, is_active=True)

    current_category = None
    current_subcategory = None

    if category_slug:
        cat = Category.query.filter_by(slug=category_slug).first()
        if cat:
            query = query.filter_by(category_id=cat.id)
            current_category = cat

    if subcategory_slug:
        subcat = SubCategory.query.filter_by(slug=subcategory_slug).first()
        if subcat:
            query = query.filter_by(sub_category_id=subcat.id)
            current_subcategory = subcat

    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))

    if min_price:
        query = query.filter(Product.price >= min_price)
    if max_price:
        query = query.filter(Product.price <= max_price)

    if sort == 'price_low':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_high':
        query = query.order_by(Product.price.desc())
    elif sort == 'rating':
        query = query.order_by(Product.average_rating.desc())
    elif sort == 'name':
        query = query.order_by(Product.name.asc())
    else:
        query = query.order_by(Product.created_at.desc())

    products = query.paginate(page=page, per_page=12, error_out=False)
    categories = Category.query.filter_by(is_active=True).all()
    subcategories = SubCategory.query.filter_by(is_active=True).all() if not category_slug else SubCategory.query.filter_by(category_id=current_category.id, is_active=True).all() if current_category else []

    return render_template('customer/products.html',
                         products=products,
                         categories=categories,
                         subcategories=subcategories,
                         category_slug=category_slug,
                         subcategory_slug=subcategory_slug,
                         search=search,
                         sort=sort,
                         current_category=current_category,
                         current_subcategory=current_subcategory)


@customer.route('/product/<slug>')
def product_detail(slug):
    product = Product.query.filter_by(slug=slug, is_approved=True).first_or_404()
    related = Product.query.filter_by(
        category_id=product.category_id, is_approved=True, is_active=True
    ).filter(Product.id != product.id).limit(4).all()

    reviews = Review.query.filter_by(
        product_id=product.id, is_approved=True
    ).order_by(Review.created_at.desc()).all()

    form = ReviewForm()
    if current_user.is_authenticated and current_user.role == 'customer':
        cust = Customer.query.filter_by(user_id=current_user.id).first()
        existing_review = Review.query.filter_by(
            product_id=product.id, customer_id=cust.id).first()
        if existing_review:
            form = None

    vendor_store = Vendor.query.get(product.vendor_id)

    return render_template('customer/product_detail.html',
                         product=product,
                         related=related,
                         reviews=reviews,
                         form=form,
                         vendor_store=vendor_store)


@customer.route('/cart')
@login_required
@customer_required
def cart():
    cust = Customer.query.filter_by(user_id=current_user.id).first()
    cart_items = Cart.query.filter_by(customer_id=cust.id).all()
    total = calculate_cart_total(cart_items)
    return render_template('customer/cart.html', cart_items=cart_items, total=total)


@customer.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
@customer_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cust = Customer.query.filter_by(user_id=current_user.id).first()

    if not product.is_active or not product.is_approved:
        flash('Product not available.', 'danger')
        return redirect(url_for('customer.product_detail', slug=product.slug))

    quantity = int(request.form.get('quantity', 1))
    existing = Cart.query.filter_by(customer_id=cust.id, product_id=product_id).first()

    if existing:
        existing.quantity += quantity
    else:
        cart_item = Cart(customer_id=cust.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    flash('Added to cart!', 'success')
    return redirect(url_for('customer.cart'))


@customer.route('/cart/update/<int:id>', methods=['POST'])
@login_required
@customer_required
def update_cart(id):
    cust = Customer.query.filter_by(user_id=current_user.id).first()
    item = Cart.query.filter_by(id=id, customer_id=cust.id).first_or_404()
    quantity = int(request.form.get('quantity', 1))
    if quantity <= 0:
        db.session.delete(item)
    else:
        item.quantity = min(quantity, item.product.stock)
    db.session.commit()
    return redirect(url_for('customer.cart'))


@customer.route('/cart/remove/<int:id>', methods=['POST'])
@login_required
@customer_required
def remove_from_cart(id):
    cust = Customer.query.filter_by(user_id=current_user.id).first()
    item = Cart.query.filter_by(id=id, customer_id=cust.id).first_or_404()
    db.session.delete(item)
    db.session.commit()
    flash('Item removed from cart.', 'info')
    return redirect(url_for('customer.cart'))


@customer.route('/checkout', methods=['GET', 'POST'])
@login_required
@customer_required
def checkout():
    cust = Customer.query.filter_by(user_id=current_user.id).first()
    cart_items = Cart.query.filter_by(customer_id=cust.id).all()

    if not cart_items or len(cart_items) == 0:
        flash('Cart is empty.', 'warning')
        return redirect(url_for('customer.cart'))

    for item in cart_items:
        if item.product.stock < item.quantity:
            flash(f'Insufficient stock for {item.product.name}', 'danger')
            return redirect(url_for('customer.cart'))

    total = calculate_cart_total(cart_items)

    if request.method == 'POST' and 'esewa' in request.form:
        shipping_address = request.form.get('shipping_address', cust.shipping_address)
        phone = request.form.get('phone', cust.phone)

        group_by_vendor = {}
        for item in cart_items:
            vid = item.product.vendor_id
            if vid not in group_by_vendor:
                group_by_vendor[vid] = []
            group_by_vendor[vid].append(item)

        orders = []
        for vid, items in group_by_vendor.items():
            vendor_total = sum(
                (i.product.discounted_price or i.product.price) * i.quantity
                for i in items
            )
            order = Order(
                order_number=generate_order_number(),
                customer_id=cust.id,
                vendor_id=vid,
                total_amount=vendor_total,
                shipping_address=shipping_address,
                phone=phone,
                status='pending'
            )
            db.session.add(order)
            db.session.flush()

            for item in items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item.product_id,
                    product_name=item.product.name,
                    quantity=item.quantity,
                    price=item.product.discounted_price or item.product.price,
                    total=(item.product.discounted_price or item.product.price) * item.quantity
                )
                db.session.add(order_item)
                product = item.product
                if product.stock >= item.quantity:
                    product.stock -= item.quantity
                db.session.delete(item)
            orders.append(order)

        db.session.commit()

        return redirect(url_for('payment.select_method', order_id=orders[0].id))

    return render_template('customer/checkout.html',
                         cart_items=cart_items, total=total, customer=cust)


@customer.route('/payment-success')
@login_required
@customer_required
def payment_success():
    order_id = request.args.get('order_id')
    order = Order.query.get_or_404(order_id)
    if order.customer.user_id != current_user.id:
        abort(403)
    flash('Payment successful! Order placed.', 'success')
    return redirect(url_for('customer.order_detail', id=order.id))


@customer.route('/orders')
@login_required
@customer_required
def orders():
    cust = Customer.query.filter_by(user_id=current_user.id).first()
    page = request.args.get('page', 1, type=int)
    user_orders = Order.query.filter_by(customer_id=cust.id).order_by(
        Order.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('customer/orders.html', orders=user_orders)


@customer.route('/order/<int:id>')
@login_required
@customer_required
def order_detail(id):
    cust = Customer.query.filter_by(user_id=current_user.id).first()
    order = Order.query.filter_by(id=id, customer_id=cust.id).first_or_404()
    return render_template('customer/order_detail.html', order=order)


@customer.route('/order/<int:id>/cancel', methods=['POST'])
@login_required
@customer_required
def cancel_order(id):
    cust = Customer.query.filter_by(user_id=current_user.id).first()
    order = Order.query.filter_by(id=id, customer_id=cust.id).first_or_404()
    if order.status in ['pending', 'processing']:
        order.status = 'cancelled'
        for item in order.items:
            product = Product.query.get(item.product_id)
            if product:
                product.stock += item.quantity
        db.session.commit()
        flash('Order cancelled.', 'info')
    else:
        flash('Order cannot be cancelled.', 'danger')
    return redirect(url_for('customer.order_detail', id=id))


@customer.route('/wishlist')
@login_required
@customer_required
def wishlist():
    cust = Customer.query.filter_by(user_id=current_user.id).first()
    wishlist_ids = []
    if cust.wishlist:
        wishlist_ids = json.loads(cust.wishlist)
    products = Product.query.filter(
        Product.id.in_(wishlist_ids), Product.is_approved == True
    ).all() if wishlist_ids else []
    return render_template('customer/wishlist.html', products=products)


@customer.route('/wishlist/toggle/<int:product_id>', methods=['POST'])
@login_required
@customer_required
def toggle_wishlist(product_id):
    cust = Customer.query.filter_by(user_id=current_user.id).first()
    wishlist = []
    if cust.wishlist:
        wishlist = json.loads(cust.wishlist)

    if product_id in wishlist:
        wishlist.remove(product_id)
        flash('Removed from wishlist.', 'info')
    else:
        wishlist.append(product_id)
        flash('Added to wishlist!', 'success')

    cust.wishlist = json.dumps(wishlist)
    db.session.commit()
    return redirect(request.referrer or url_for('customer.home'))


@customer.route('/profile', methods=['GET', 'POST'])
@login_required
@customer_required
def profile():
    cust = Customer.query.filter_by(user_id=current_user.id).first()
    form = CustomerProfileForm(obj=cust)
    if form.validate_on_submit():
        cust.full_name = form.full_name.data
        cust.phone = form.phone.data
        cust.address = form.address.data
        cust.city = form.city.data
        cust.shipping_address = form.shipping_address.data
        if form.avatar.data and hasattr(form.avatar.data, 'filename'):
            cust.avatar = save_image(form.avatar.data, 'avatars')
        db.session.commit()
        flash('Profile updated.', 'success')
        return redirect(url_for('customer.profile'))
    return render_template('customer/profile.html', form=form, customer=cust)


@customer.route('/review/add/<int:product_id>', methods=['POST'])
@login_required
@customer_required
def add_review(product_id):
    product = Product.query.get_or_404(product_id)
    cust = Customer.query.filter_by(user_id=current_user.id).first()

    existing = Review.query.filter_by(product_id=product_id, customer_id=cust.id).first()
    if existing:
        flash('You already reviewed this product.', 'warning')
        return redirect(url_for('customer.product_detail', slug=product.slug))

    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            product_id=product_id,
            customer_id=cust.id,
            rating=form.rating.data,
            title=form.title.data,
            comment=form.comment.data
        )
        db.session.add(review)

        reviews = Review.query.filter_by(product_id=product_id).all()
        avg = sum(r.rating for r in reviews) / (len(reviews) + 1)
        product.average_rating = round((product.average_rating * product.review_count + form.rating.data) / (product.review_count + 1), 1)
        product.review_count += 1
        db.session.commit()
        flash('Review submitted!', 'success')

    return redirect(url_for('customer.product_detail', slug=product.slug))


@customer.route('/api/subcategories/<int:category_id>')
def api_subcategories(category_id):
    subcats = SubCategory.query.filter_by(category_id=category_id, is_active=True).all()
    return jsonify([{'id': s.id, 'name': s.name, 'slug': s.slug} for s in subcats])


@customer.route('/category/<slug>')
def category_products(slug):
    cat = Category.query.filter_by(slug=slug, is_active=True).first_or_404()
    page = request.args.get('page', 1, type=int)
    subcategory_slug = request.args.get('subcategory')
    query = Product.query.filter_by(category_id=cat.id, is_approved=True, is_active=True)

    if subcategory_slug:
        subcat = SubCategory.query.filter_by(slug=subcategory_slug, category_id=cat.id).first()
        if subcat:
            query = query.filter_by(sub_category_id=subcat.id)

    products = query.order_by(Product.created_at.desc()).paginate(page=page, per_page=12)
    categories = Category.query.filter_by(is_active=True).all()
    subcategories = SubCategory.query.filter_by(category_id=cat.id, is_active=True).all()
    return render_template('customer/products.html',
                         products=products,
                         categories=categories,
                         subcategories=subcategories,
                         current_category=cat,
                         subcategory_slug=subcategory_slug)
