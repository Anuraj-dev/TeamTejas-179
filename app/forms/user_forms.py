from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional

class EditProfileForm(FlaskForm):
    """Form for editing user profile."""
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=3, max=80)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(max=120)
    ])
    profile_image = FileField('Profile Image', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    new_password = PasswordField('New Password', validators=[
        Optional(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        EqualTo('new_password', message='Passwords must match')
    ])
