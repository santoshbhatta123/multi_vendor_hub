from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from app.models.user import User
from app.models.vendor import Vendor
from app.models.customer import Customer
from app.forms.auth_forms import RegistrationForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from app.utils.decorators import redirect_authenticated_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
@redirect_authenticated_user
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('Your account has been deactivated.', 'danger')
                return render_template('auth/login.html', form=form)
            login_user(user, remember=form.remember.data)
            user.last_login = db.func.now()
            db.session.commit()
            next_page = request.args.get('next')
            if user.role == 'admin':
                return redirect(next_page or url_for('admin.dashboard'))
            elif user.role == 'vendor':
                return redirect(next_page or url_for('vendor.dashboard'))
            else:
                return redirect(next_page or url_for('customer.home'))
        flash('Invalid email or password.', 'danger')
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
@redirect_authenticated_user
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()

        if form.role.data == 'vendor':
            vendor = Vendor(
                user_id=user.id,
                store_name=form.username.data + "'s Store",
                store_slug=form.username.data.lower().replace(' ', '-')
            )
            db.session.add(vendor)
        else:
            customer = Customer(
                user_id=user.id,
                full_name=form.username.data
            )
            db.session.add(customer)

        db.session.commit()
        flash(f'Account created! You can now log in as {form.role.data}.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Password reset link has been sent to your email.', 'info')
        else:
            flash('No account found with that email.', 'danger')
    return render_template('auth/forgot_password.html', form=form)


@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm()
    if form.validate_on_submit():
        flash('Your password has been reset. Please login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
