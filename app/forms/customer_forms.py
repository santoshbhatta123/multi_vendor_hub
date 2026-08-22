from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Optional, NumberRange


class CustomerProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[Optional(), Length(max=100)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    address = TextAreaField('Address', validators=[Optional()])
    city = StringField('City', validators=[Optional(), Length(max=100)])
    shipping_address = TextAreaField('Shipping Address', validators=[Optional()])
    avatar = FileField('Profile Picture', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')])
    submit = SubmitField('Update Profile')


class ReviewForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    title = StringField('Title', validators=[Optional(), Length(max=200)])
    comment = TextAreaField('Review', validators=[Optional()])
    submit = SubmitField('Submit Review')
