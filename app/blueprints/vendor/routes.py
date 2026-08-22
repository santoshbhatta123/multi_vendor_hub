from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, current_app, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.vendor import Vendor
from app.models.product import Product
from app.models.category import Category
from app.models.subcategory import SubCategory
from app.models.order import Order, OrderItem
from app.models.payment import Payment
from app.models.review import Review
from app.forms.vendor_forms import VendorProfileForm, ProductForm
from app.utils.decorators import vendor_required
from app.utils.helpers import save_image, generate_order_number
from datetime import datetime, timedelta
from sqlalchemy import func
import os

vendor = Blueprint('vendor', __name__)


@vendor.before_request
@login_required
@vendor_required
def before_request():
    pass


def get_vendor():
    return Vendor.query.filter_by(user_id=current_user.id).first_or_404()


@vendor.route('/dashboard')
def dashboard():
    v = get_vendor()
    total_products = Product.query.filter_by(vendor_id=v.id).count()
    total_orders = Order.query.filter_by(vendor_id=v.id).count()
    total_revenue = db.session.query(func.sum(Order.total_amount)).filter(
        Order.vendor_id == v.id,
        Order.payment_status == 'paid'
    ).scalar() or 0
    pending_orders = Order.query.filter_by(vendor_id=v.id, status='pending').count()

    recent_orders = Order.query.filter_by(vendor_id=v.id).order_by(
        Order.created_at.desc()).limit(5).all()
    low_stock = Product.query.filter(
        Product.vendor_id == v.id,
        Product.stock <= 5,
        Product.is_active == True
    ).all()

    monthly_sales = db.session.query(
        func.sum(OrderItem.total),
        func.extract('month', OrderItem.id)
    ).join(Order, Order.id == OrderItem.order_id).filter(
        Order.vendor_id == v.id,
        Order.payment_status == 'paid',
        Order.created_at >= datetime.utcnow() - timedelta(days=30)
    ).first()

    context = {
        'vendor': v,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'pending_orders': pending_orders,
        'recent_orders': recent_orders,
        'low_stock': low_stock,
        'monthly_sales': monthly_sales[0] if monthly_sales and monthly_sales[0] else 0,
    }
    return render_template('vendor/dashboard.html', **context)


@vendor.route('/profile', methods=['GET', 'POST'])
def profile():
    v = get_vendor()
    form = VendorProfileForm(obj=v)
    if form.validate_on_submit():
        v.store_name = form.store_name.data
        v.store_description = form.store_description.data
        v.phone = form.phone.data
        v.address = form.address.data
        v.city = form.city.data
        if form.store_logo.data and hasattr(form.store_logo.data, 'filename'):
            v.store_logo = save_image(form.store_logo.data)
        if form.store_banner.data and hasattr(form.store_banner.data, 'filename'):
            v.store_banner = save_image(form.store_banner.data)
        db.session.commit()
        flash('Profile updated.', 'success')
        return redirect(url_for('vendor.profile'))
    return render_template('vendor/profile.html', form=form, vendor=v)


@vendor.route('/products')
def products():
    v = get_vendor()
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter_by(vendor_id=v.id).order_by(
        Product.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('vendor/products.html', products=products, vendor=v)


@vendor.route('/product/add', methods=['GET', 'POST'])
def add_product():
    v = get_vendor()
    form = ProductForm()
    if form.validate_on_submit():
        sub_cat_id = form.sub_category_id.data if form.sub_category_id.data and form.sub_category_id.data != 0 else None
        product = Product(
            vendor_id=v.id,
            category_id=form.category_id.data,
            sub_category_id=sub_cat_id,
            name=form.name.data,
            slug=form.name.data.lower().replace(' ', '-') + '-' + str(datetime.utcnow().timestamp()).split('.')[0],
            description=form.description.data,
            price=form.price.data,
            discounted_price=form.discounted_price.data or None,
            stock=form.stock.data,
            is_featured=form.is_featured.data,
            is_approved=True,
            status='active'
        )
        if form.image_1.data and hasattr(form.image_1.data, 'filename'):
            product.image_1 = save_image(form.image_1.data)
        if form.image_2.data and hasattr(form.image_2.data, 'filename'):
            product.image_2 = save_image(form.image_2.data)
        if form.image_3.data and hasattr(form.image_3.data, 'filename'):
            product.image_3 = save_image(form.image_3.data)
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('vendor.products'))
    return render_template('vendor/product_form.html', form=form, title='Add Product')


@vendor.route('/product/<int:id>/edit', methods=['GET', 'POST'])
def edit_product(id):
    v = get_vendor()
    product = Product.query.filter_by(id=id, vendor_id=v.id).first_or_404()
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.category_id = form.category_id.data
        product.sub_category_id = form.sub_category_id.data if form.sub_category_id.data and form.sub_category_id.data != 0 else None
        product.description = form.description.data
        product.price = form.price.data
        product.discounted_price = form.discounted_price.data or None
        product.stock = form.stock.data
        product.is_featured = form.is_featured.data
        if form.image_1.data and hasattr(form.image_1.data, 'filename'):
            product.image_1 = save_image(form.image_1.data)
        if form.image_2.data and hasattr(form.image_2.data, 'filename'):
            product.image_2 = save_image(form.image_2.data)
        if form.image_3.data and hasattr(form.image_3.data, 'filename'):
            product.image_3 = save_image(form.image_3.data)
        product.is_approved = True
        product.status = 'active'
        db.session.commit()
        flash('Product updated.', 'success')
        return redirect(url_for('vendor.products'))
    if product.sub_category_id:
        form.sub_category_id.data = product.sub_category_id
    return render_template('vendor/product_form.html', form=form, title='Edit Product')


@vendor.route('/product/<int:id>/delete', methods=['POST'])
def delete_product(id):
    v = get_vendor()
    product = Product.query.filter_by(id=id, vendor_id=v.id).first_or_404()
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted.', 'info')
    return redirect(url_for('vendor.products'))


@vendor.route('/product/<int:id>/toggle', methods=['POST'])
def toggle_product(id):
    v = get_vendor()
    product = Product.query.filter_by(id=id, vendor_id=v.id).first_or_404()
    product.is_active = not product.is_active
    db.session.commit()
    flash(f'Product {"activated" if product.is_active else "deactivated"}.', 'info')
    return redirect(url_for('vendor.products'))


@vendor.route('/orders')
def orders():
    v = get_vendor()
    page = request.args.get('page', 1, type=int)
    orders = Order.query.filter_by(vendor_id=v.id).order_by(
        Order.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('vendor/orders.html', orders=orders, vendor=v)


@vendor.route('/order/<int:id>')
def order_detail(id):
    v = get_vendor()
    order = Order.query.filter_by(id=id, vendor_id=v.id).first_or_404()
    return render_template('vendor/order_detail.html', order=order, vendor=v)


@vendor.route('/order/<int:id>/status', methods=['POST'])
def update_order_status(id):
    v = get_vendor()
    order = Order.query.filter_by(id=id, vendor_id=v.id).first_or_404()
    new_status = request.form.get('status')
    if new_status in ['processing', 'shipped', 'delivered', 'cancelled']:
        allowed_transitions = {
            'pending': ['processing', 'cancelled'],
            'processing': ['shipped', 'cancelled'],
            'shipped': ['delivered', 'cancelled'],
        }
        if order.status in allowed_transitions and new_status in allowed_transitions[order.status]:
            order.status = new_status
            if new_status == 'delivered':
                order.payment_status = 'paid'
                product = Product.query.get(order.items[0].product_id)
                if product:
                    product.sold_count += 1
            db.session.commit()
            flash(f'Order status updated to {new_status}.', 'success')
        else:
            flash('Invalid status transition.', 'danger')
    return redirect(url_for('vendor.order_detail', id=id))


@vendor.route('/earnings')
def earnings():
    v = get_vendor()
    total_earned = db.session.query(func.sum(Order.total_amount)).filter(
        Order.vendor_id == v.id,
        Order.payment_status == 'paid'
    ).scalar() or 0
    pending_amount = db.session.query(func.sum(Order.total_amount)).filter(
        Order.vendor_id == v.id,
        Order.payment_status == 'unpaid'
    ).scalar() or 0

    monthly_data = db.session.query(
        func.sum(Order.total_amount),
        func.date_format(Order.created_at, '%Y-%m')
    ).filter(
        Order.vendor_id == v.id,
        Order.payment_status == 'paid'
    ).group_by(func.date_format(Order.created_at, '%Y-%m')).order_by(
        func.date_format(Order.created_at, '%Y-%m')).all()

    recent_payments = Order.query.filter_by(
        vendor_id=v.id, payment_status='paid'
    ).order_by(Order.created_at.desc()).limit(10).all()

    return render_template('vendor/earnings.html',
                         vendor=v,
                         total_earned=total_earned,
                         pending_amount=pending_amount,
                         monthly_data=monthly_data,
                         recent_payments=recent_payments)


@vendor.route('/api/subcategories/<int:category_id>')
def api_subcategories(category_id):
    subcats = SubCategory.query.filter_by(category_id=category_id, is_active=True).all()
    return jsonify([{'id': s.id, 'name': s.name} for s in subcats])


@vendor.route('/reviews')
def reviews():
    v = get_vendor()
    product_ids = [p.id for p in Product.query.filter_by(vendor_id=v.id).all()]
    reviews = Review.query.filter(Review.product_id.in_(product_ids)).order_by(
        Review.created_at.desc()).all()
    return render_template('vendor/reviews.html', reviews=reviews, vendor=v)
