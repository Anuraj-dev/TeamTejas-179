import os
from flask import Flask
from datetime import datetime
from flask_login import current_user

from app.extensions import init_extensions
from app.config.config import config


def create_app(config_name=None):
    """Create Flask application using the app factory pattern."""
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    init_extensions(app)
    
    # Configure logging
    from app.logger import configure_logging
    configure_logging(app)
    
    # Configure security features
    from app.security import configure_security
    configure_security(app)
    
    # Register error handlers
    from app.errors import register_error_handlers
    register_error_handlers(app)
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.products import products_bp
    from app.routes.user import user_bp
    from app.routes.cart import cart_bp
    from app.routes.purchase import purchase_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(purchase_bp)
    
    # Register CLI commands
    from app.cli import register_commands
    register_commands(app)
    
    # Inject datetime utility into templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}
    
    @app.context_processor
    def utility_processor():
        cart_count = 0
        if current_user.is_authenticated and current_user.cart:
            cart_count = current_user.cart.items.count() if hasattr(current_user.cart, 'items') else 0
            
        return {'cart_item_count': cart_count}
    
    app.logger.info('Application initialized with configuration: %s', config_name)
    
    return app
