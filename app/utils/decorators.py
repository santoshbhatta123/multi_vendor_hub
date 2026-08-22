from functools import wraps
from flask import abort, redirect, url_for, flash
from flask_login import current_user


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def vendor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'vendor':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def customer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'customer':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def redirect_authenticated_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif current_user.role == 'vendor':
                return redirect(url_for('vendor.dashboard'))
            else:
                return redirect(url_for('customer.home'))
        return f(*args, **kwargs)
    return decorated_function
