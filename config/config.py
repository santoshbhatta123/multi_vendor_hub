import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'multi-vendor-hub-secret-key-2025'
 database_url = os.environ.get('DATABASE_URL')

if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace(
        'postgres://',
        'postgresql://',
        1
    )

SQLALCHEMY_DATABASE_URI = database_url or \
    'sqlite:///multi_vendor_hub.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    REMEMBER_COOKIE_DURATION = timedelta(days=7)

    # File upload config
    UPLOAD_FOLDER = os.path.join(basedir, '..', 'app', 'static', 'vendor_images')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # Pagination
    PRODUCTS_PER_PAGE = 12

    # Mail config
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or ''
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or ''
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@multivendorhub.com'

    # ── eSewa ePay V2 config ─────────────────────────────────
    # Environment: 'UAT' (development/test) or 'PRODUCTION'
    ESEWA_ENVIRONMENT = os.environ.get('ESEWA_ENVIRONMENT') or 'UAT'
    _IS_PROD = ESEWA_ENVIRONMENT == 'PRODUCTION'

    # UAT / Test credentials (official eSewa test merchant)
    ESEWA_UAT_PRODUCT_CODE = 'EPAYTEST'
    ESEWA_UAT_SECRET_KEY = '8gBm/:&EnhH.1/q'
    ESEWA_UAT_PAYMENT_URL = 'https://rc-epay.esewa.com.np/api/epay/main/v2/form'
    ESEWA_UAT_VERIFY_URL = 'https://rc.esewa.com.np/api/epay/transaction/status/'

    # Production credentials (DO NOT use for the project demo)
    ESEWA_PROD_PRODUCT_CODE = os.environ.get('ESEWA_PROD_PRODUCT_CODE') or ''
    ESEWA_PROD_SECRET_KEY = os.environ.get('ESEWA_PROD_SECRET_KEY') or ''
    ESEWA_PROD_PAYMENT_URL = 'https://epay.esewa.com.np/api/epay/main/v2/form'
    ESEWA_PROD_VERIFY_URL = 'https://epay.esewa.com.np/api/epay/transaction/status/'

    # Active values selected by ESEWA_ENVIRONMENT
    ESEWA_PRODUCT_CODE = ESEWA_PROD_PRODUCT_CODE if _IS_PROD else ESEWA_UAT_PRODUCT_CODE
    ESEWA_SECRET_KEY = ESEWA_PROD_SECRET_KEY if _IS_PROD else ESEWA_UAT_SECRET_KEY
    ESEWA_PAYMENT_URL = ESEWA_PROD_PAYMENT_URL if _IS_PROD else ESEWA_UAT_PAYMENT_URL
    ESEWA_VERIFY_URL = ESEWA_PROD_VERIFY_URL if _IS_PROD else ESEWA_UAT_VERIFY_URL
