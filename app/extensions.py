from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
# Create a fallback implementation in case flask_bcrypt isn't available
try:
    from flask_bcrypt import Bcrypt
except ImportError:
    import hashlib
    import os
    
    class FallbackBcrypt:
        """
        A minimal fallback implementation of Bcrypt when the actual package is not available.
        This is NOT secure for production and should only be used during development.
        """
        def __init__(self, app=None):
            self.app = app
            if app is not None:
                self.init_app(app)
        
        def init_app(self, app):
            self.app = app
            app.extensions['bcrypt'] = self
        
        def generate_password_hash(self, password, rounds=12):
            salt = os.urandom(16).hex()
            pw_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            return f'$fallback${rounds}${salt}${pw_hash}'.encode('utf-8')
        
        def check_password_hash(self, pw_hash, password):
            if not pw_hash.startswith(b'$fallback$'):
                return False
            parts = pw_hash.decode('utf-8').split('$')
            if len(parts) != 5:
                return False
            _, _, rounds, salt, stored_hash = parts
            check_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            return check_hash == stored_hash
    
    Bcrypt = FallbackBcrypt
    print("WARNING: Using insecure password hashing fallback. Install flask_bcrypt for production use.")

from flask_mail import Mail

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
bcrypt = Bcrypt()
mail = Mail()

def init_extensions(app):
    """Initialize Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))
    
    return app
