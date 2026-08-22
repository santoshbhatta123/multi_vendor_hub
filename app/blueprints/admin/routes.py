from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.vendor import Vendor
from app.models.customer import Customer
from app.models.product import Product
from app.models.category import Category
from app.models.subcategory import SubCategory
from app.models.order import Order, OrderItem
from app.models.payment import Payment
from app.models.review import Review
from app.forms.admin_forms import CategoryForm, SubCategoryForm
from app.utils.decorators import admin_required
from app.utils.helpers import save_image
from datetime import datetime, timedelta
from sqlalchemy import func

admin = Blueprint('admin', __name__)


@admin.before_request
@login_required
@admin_required
def before_request():
    pass


@admin.route('/dashboard')
def dashboard():
    total_users = User.query.count()
    total_vendors = Vendor.query.count()
    total_customers = Customer.query.count()
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(func.sum(Order.total_amount)).filter(
        Order.payment_status == 'paid').scalar() or 0
    pending_products = Product.query.filter_by(status='pending').count()

    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()

    monthly_revenue = db.session.query(
        func.sum(Order.total_amount),
        func.extract('month', Order.created_at)
    ).filter(
        Order.payment_status == 'paid',
        Order.created_at >= datetime.utcnow() - timedelta(days=30)
    ).group_by(func.extract('month', Order.created_at)).first()

    context = {
        'total_users': total_users,
        'total_vendors': total_vendors,
        'total_customers': total_customers,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'pending_products': pending_products,
        'recent_orders': recent_orders,
        'recent_users': recent_users,
        'monthly_revenue': monthly_revenue[0] if monthly_revenue else 0,
    }
    return render_template('admin/dashboard.html', **context)


@admin.route('/vendors')
def vendors():
    vendors = Vendor.query.order_by(Vendor.created_at.desc()).all()
    return render_template('admin/vendors.html', vendors=vendors)


@admin.route('/vendor/<int:id>/approve')
def approve_vendor(id):
    vendor = Vendor.query.get_or_404(id)
    vendor.is_approved = True
    vendor.is_verified = True
    db.session.commit()
    flash(f'Vendor {vendor.store_name} has been approved.', 'success')
    return redirect(url_for('admin.vendors'))


@admin.route('/vendor/<int:id>/suspend')
def suspend_vendor(id):
    vendor = Vendor.query.get_or_404(id)
    user = User.query.get(vendor.user_id)
    user.is_active = not user.is_active
    db.session.commit()
    status = 'suspended' if not user.is_active else 'reactivated'
    flash(f'Vendor has been {status}.', 'info')
    return redirect(url_for('admin.vendors'))


@admin.route('/customers')
def customers():
    customers = Customer.query.order_by(Customer.created_at.desc()).all()
    return render_template('admin/customers.html', customers=customers)


@admin.route('/products')
def products():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('admin/products.html', products=products)


@admin.route('/product/<int:id>/approve', methods=['POST'])
def approve_product(id):
    product = Product.query.get_or_404(id)
    product.is_approved = True
    product.status = 'approved'
    db.session.commit()
    flash(f'Product {product.name} has been approved.', 'success')
    return redirect(url_for('admin.products'))


@admin.route('/product/<int:id>/reject', methods=['POST'])
def reject_product(id):
    product = Product.query.get_or_404(id)
    product.status = 'rejected'
    db.session.commit()
    flash(f'Product {product.name} has been rejected.', 'warning')
    return redirect(url_for('admin.products'))


@admin.route('/product/<int:id>/delete', methods=['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted.', 'info')
    return redirect(url_for('admin.products'))


@admin.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)


@admin.route('/category/add', methods=['GET', 'POST'])
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        from slugify import slugify
        category = Category(
            name=form.name.data,
            slug=slugify(form.name.data),
            description=form.description.data,
            is_active=form.is_active.data
        )
        if form.image.data and hasattr(form.image.data, 'filename'):
            category.image = save_image(form.image.data, 'category_images')
        db.session.add(category)
        db.session.commit()
        flash('Category added.', 'success')
        return redirect(url_for('admin.categories'))
    return render_template('admin/category_form.html', form=form, title='Add Category')


@admin.route('/category/<int:id>/edit', methods=['GET', 'POST'])
def edit_category(id):
    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        category.is_active = form.is_active.data
        if form.image.data and hasattr(form.image.data, 'filename'):
            category.image = save_image(form.image.data, 'category_images')
        db.session.commit()
        flash('Category updated.', 'success')
        return redirect(url_for('admin.categories'))
    return render_template('admin/category_form.html', form=form, title='Edit Category')


@admin.route('/orders')
def orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)


@admin.route('/order/<int:id>')
def order_detail(id):
    order = Order.query.get_or_404(id)
    return render_template('admin/order_detail.html', order=order)


@admin.route('/order/<int:id>/status', methods=['POST'])
def update_order_status(id):
    order = Order.query.get_or_404(id)
    status = request.form.get('status')
    if status in ['pending', 'processing', 'shipped', 'delivered', 'cancelled']:
        order.status = status
        if status == 'delivered':
            order.payment_status = 'paid'
        db.session.commit()
        flash(f'Order status updated to {status}.', 'success')
    return redirect(url_for('admin.order_detail', id=id))


@admin.route('/reports')
def reports():
    total_revenue = db.session.query(func.sum(Order.total_amount)).filter(
        Order.payment_status == 'paid').scalar() or 0
    total_orders = Order.query.count()
    total_products = Product.query.count()
    total_vendors = Vendor.query.count()

    top_vendors = db.session.query(
        Vendor, func.sum(Order.total_amount).label('revenue')
    ).join(Order, Order.vendor_id == Vendor.id).filter(
        Order.payment_status == 'paid'
    ).group_by(Vendor.id).order_by(db.text('revenue DESC')).limit(5).all()

    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()

    return render_template('admin/reports.html',
                         total_revenue=total_revenue,
                         total_orders=total_orders,
                         total_products=total_products,
                         total_vendors=total_vendors,
                         top_vendors=top_vendors,
                         recent_orders=recent_orders)


@admin.route('/subcategories')
def subcategories():
    subcats = SubCategory.query.order_by(SubCategory.category_id, SubCategory.name).all()
    return render_template('admin/subcategories.html', subcategories=subcats)


@admin.route('/subcategory/add', methods=['GET', 'POST'])
def add_subcategory():
    form = SubCategoryForm()
    if form.validate_on_submit():
        from slugify import slugify
        subcat = SubCategory(
            category_id=form.category_id.data,
            name=form.name.data,
            slug=slugify(form.name.data),
            description=form.description.data,
            is_active=form.is_active.data
        )
        db.session.add(subcat)
        db.session.commit()
        flash('Subcategory added.', 'success')
        return redirect(url_for('admin.subcategories'))
    return render_template('admin/subcategory_form.html', form=form, title='Add Subcategory')


@admin.route('/subcategory/<int:id>/edit', methods=['GET', 'POST'])
def edit_subcategory(id):
    subcat = SubCategory.query.get_or_404(id)
    form = SubCategoryForm(obj=subcat)
    if form.validate_on_submit():
        from slugify import slugify
        subcat.category_id = form.category_id.data
        subcat.name = form.name.data
        subcat.slug = slugify(form.name.data)
        subcat.description = form.description.data
        subcat.is_active = form.is_active.data
        db.session.commit()
        flash('Subcategory updated.', 'success')
        return redirect(url_for('admin.subcategories'))
    return render_template('admin/subcategory_form.html', form=form, title='Edit Subcategory')


@admin.route('/subcategory/<int:id>/delete', methods=['POST'])
def delete_subcategory(id):
    subcat = SubCategory.query.get_or_404(id)
    db.session.delete(subcat)
    db.session.commit()
    flash('Subcategory deleted.', 'info')
    return redirect(url_for('admin.subcategories'))


@admin.route('/reviews')
def reviews():
    reviews = Review.query.order_by(Review.created_at.desc()).all()
    return render_template('admin/reviews.html', reviews=reviews)


@admin.route('/review/<int:id>/approve', methods=['POST'])
def approve_review(id):
    review = Review.query.get_or_404(id)
    review.is_approved = True
    db.session.commit()
    flash('Review approved.', 'success')
    return redirect(url_for('admin.reviews'))
