from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileSize
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from app.models.category import Category


class VendorProfileForm(FlaskForm):
    store_name = StringField('Store Name', validators=[DataRequired(), Length(max=100)])
    store_description = TextAreaField('Store Description', validators=[Optional()])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    address = TextAreaField('Address', validators=[Optional()])
    city = StringField('City', validators=[Optional(), Length(max=100)])
    store_logo = FileField('Store Logo', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')])
    store_banner = FileField('Store Banner', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')])
    submit = SubmitField('Update Profile')


class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[Optional()])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    discounted_price = FloatField('Discounted Price', validators=[Optional(), NumberRange(min=0)])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)], default=0)
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    sub_category_id = SelectField('Subcategory', coerce=int, validators=[Optional()], default=0, validate_choice=False)
    image_1 = FileField('Main Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')])
    image_2 = FileField('Additional Image 1', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')])
    image_3 = FileField('Additional Image 2', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')])
    is_featured = BooleanField('Feature this product')
    submit = SubmitField('Save Product')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(c.id, c.name) for c in Category.query.filter_by(is_active=True).all()]
        self.sub_category_id.choices = [(0, '-- Select Subcategory (optional) --')]
