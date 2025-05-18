import re
from datetime import datetime
from wtforms.validators import ValidationError

# Regular expression patterns
EMAIL_PATTERN = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
PHONE_PATTERN = r'^\+?[0-9]{10,15}$'
USERNAME_PATTERN = r'^[a-zA-Z0-9_]{3,20}$'
PASSWORD_PATTERN = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$'

def validate_email(email):
    """
    Validate email format.
    
    Args:
        email: Email string to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not email:
        return False
    return bool(re.match(EMAIL_PATTERN, email))

def validate_password_strength(password):
    """
    Validate password strength.
    
    Args:
        password: Password to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not password:
        return False
    return bool(re.match(PASSWORD_PATTERN, password))

def validate_phone(phone):
    """
    Validate phone number format.
    
    Args:
        phone: Phone number to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not phone:
        return False
    return bool(re.match(PHONE_PATTERN, phone))

def validate_username(username):
    """
    Validate username format.
    
    Args:
        username: Username to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not username:
        return False
    return bool(re.match(USERNAME_PATTERN, username))

def validate_date_format(date_str, format='%Y-%m-%d'):
    """
    Validate date string format.
    
    Args:
        date_str: Date string to validate
        format: Expected date format
        
    Returns:
        True if valid, False otherwise
    """
    if not date_str:
        return False
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False

# Custom WTForms validators
class StrongPassword:
    """
    Custom validator for WTForms to check password strength.
    """
    def __init__(self, message=None):
        self.message = message or 'Password must be at least 8 characters with at least one letter and one number.'
    
    def __call__(self, form, field):
        if not validate_password_strength(field.data):
            raise ValidationError(self.message)

class ValidUsername:
    """
    Custom validator for WTForms to check username format.
    """
    def __init__(self, message=None):
        self.message = message or 'Username must be 3-20 characters and contain only letters, numbers, and underscores.'
    
    def __call__(self, form, field):
        if not validate_username(field.data):
            raise ValidationError(self.message)

class ValidPhone:
    """
    Custom validator for WTForms to check phone number format.
    """
    def __init__(self, message=None):
        self.message = message or 'Please enter a valid phone number.'
    
    def __call__(self, form, field):
        if field.data and not validate_phone(field.data):
            raise ValidationError(self.message)
