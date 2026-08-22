from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, Optional
from app.models.category import Category


class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional()])
    image = FileField('Category Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')])
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save Category')


class SubCategoryForm(FlaskForm):
    category_id = SelectField('Parent Category', coerce=int, validators=[DataRequired()])
    name = StringField('Subcategory Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional()])
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save Subcategory')

    def __init__(self, *args, **kwargs):
        super(SubCategoryForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(c.id, c.name) for c in Category.query.filter_by(is_active=True).all()]
