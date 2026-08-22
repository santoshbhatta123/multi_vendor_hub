import os
import secrets
from PIL import Image
from flask import current_app


def save_image(form_image, folder='vendor_images'):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_filename = random_hex + f_ext
    image_path = os.path.join(current_app.root_path, 'static', folder, image_filename)

    output_size = (800, 800)
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(image_path)

    return image_filename


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def calculate_cart_total(cart_items):
    total = 0
    for item in cart_items:
        if item.product:
            price = item.product.discounted_price or item.product.price
            total += price * item.quantity
    return total


def generate_order_number():
    import string
    import random
    return 'ORD-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
