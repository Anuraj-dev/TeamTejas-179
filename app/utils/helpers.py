import re
import random
import string
from datetime import datetime
from flask import url_for, current_app
from markupsafe import Markup

def slugify(text):
    """
    Convert a string to a URL-friendly slug.
    
    Args:
        text: String to convert
        
    Returns:
        Slugified string
    """
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text

def generate_random_string(length=10):
    """
    Generate a random string of fixed length.
    
    Args:
        length: Length of the random string
        
    Returns:
        Random string
    """
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def format_datetime(date_value, format='%B %d, %Y at %I:%M %p'):
    """
    Format a datetime object.
    
    Args:
        date_value: Datetime object to format
        format: Format string
        
    Returns:
        Formatted date string
    """
    if isinstance(date_value, str):
        try:
            date_value = datetime.strptime(date_value, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return date_value
            
    if isinstance(date_value, datetime):
        return date_value.strftime(format)
    return date_value

def format_currency(amount, currency='$'):
    """
    Format a number as currency.
    
    Args:
        amount: Amount to format
        currency: Currency symbol
        
    Returns:
        Formatted currency string
    """
    try:
        return f"{currency}{float(amount):.2f}"
    except (ValueError, TypeError):
        return f"{currency}0.00"

def truncate_text(text, length=100, suffix='...'):
    """
    Truncate text to a specified length.
    
    Args:
        text: Text to truncate
        length: Maximum length
        suffix: String to append to truncated text
        
    Returns:
        Truncated text
    """
    if not text:
        return ''
    if len(text) <= length:
        return text
    return text[:length].rsplit(' ', 1)[0] + suffix

def is_safe_url(target):
    """
    Check if URL is safe for redirects.
    
    Args:
        target: URL to check
        
    Returns:
        True if safe, False otherwise
    """
    from urllib.parse import urlparse, urljoin
    from flask import request
    
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def get_pagination_urls(pagination, endpoint, **kwargs):
    """
    Get pagination URLs for templates.
    
    Args:
        pagination: SQLAlchemy pagination object
        endpoint: Flask endpoint for URLs
        **kwargs: Additional arguments for url_for
        
    Returns:
        Dictionary with next and prev URLs
    """
    urls = {'next': None, 'prev': None}
    
    if pagination.has_next:
        kwargs['page'] = pagination.next_num
        urls['next'] = url_for(endpoint, **kwargs)
        
    if pagination.has_prev:
        kwargs['page'] = pagination.prev_num
        urls['prev'] = url_for(endpoint, **kwargs)
        
    return urls
