from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

class ProductForm(FlaskForm):
    """Form for creating and editing products."""
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=2000)])
    price = DecimalField('Price ($)', validators=[DataRequired(), NumberRange(min=0.01)], places=2)
    category_id = SelectField('Category', validators=[DataRequired()], coerce=int)
    image = FileField('Product Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])

class ProductEditForm(ProductForm):
    """Form for editing products with additional status fields."""
    is_active = BooleanField('Active (visible to buyers)')
    is_sold = BooleanField('Mark as sold')
    delete_image = BooleanField('Delete current image')
