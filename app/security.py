from flask import request, current_app, Response, g
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import functools
import time

# Initialize rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def configure_security(app):
    """Configure security features for the Flask application."""
    # Initialize rate limiter with the app
    limiter.init_app(app)
    
    # Add security headers to all responses
    @app.after_request
    def add_security_headers(response):
        """Add security headers to all responses."""
        # Content Security Policy (CSP)
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "img-src 'self' data:; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "frame-ancestors 'none'; "
            "form-action 'self'"
        )
        
        # Other security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        return response
    
    # Track request processing time
    @app.before_request
    def start_timer():
        """Start timing the request processing."""
        g.start = time.time()
    
    @app.after_request
    def log_request_time(response):
        """Log the time taken to process the request."""
        if hasattr(g, 'start'):
            total_time = time.time() - g.start
            app.logger.debug(f"Request processed in {total_time:.4f} seconds")
        return response
    
    # Apply rate limits to specific routes
    apply_auth_rate_limits(app)
    
    return app

def apply_auth_rate_limits(app):
    """Apply rate limits to authentication endpoints."""
    # Example: Rate limit login attempts
    login_limiter = limiter.shared_limit("5 per minute", scope="login")
    register_limiter = limiter.shared_limit("3 per minute", scope="register")
    
    # Apply rate limiter to routes (will need to be adjusted based on your actual route paths)
    from app.routes.auth import auth_bp
    
    # Find the view function for login and register
    for endpoint, view_func in auth_bp.view_functions.items():
        if endpoint == 'login':
            auth_bp.view_functions[endpoint] = login_limiter(view_func)
        elif endpoint == 'register':
            auth_bp.view_functions[endpoint] = register_limiter(view_func)

# Decorator for routes that handle sensitive operations
def require_secure_channel(f):
    """Ensure that sensitive operations are performed over HTTPS."""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if current_app.config.get('REQUIRE_HTTPS', False) and not request.is_secure:
            return Response("Secure connection required", status=403)
        return f(*args, **kwargs)
    return decorated_function 