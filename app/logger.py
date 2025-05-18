import os
import logging
from logging.handlers import RotatingFileHandler
from flask import request

def configure_logging(app):
    """Configure logging for the Flask application."""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Set log level based on environment
    log_level = logging.DEBUG if app.debug else logging.INFO
    
    # Configure rotating file handler
    file_handler = RotatingFileHandler(
        'logs/ecofinds.log', 
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(log_level)
    
    # Add handlers to app logger
    app.logger.addHandler(file_handler)
    app.logger.setLevel(log_level)
    
    # Log application startup
    app.logger.info('EcoFinds startup')
    
    # Configure request logging middleware
    @app.before_request
    def log_request_info():
        """Log request information before processing."""
        if not request.path.startswith('/static/'):
            app.logger.debug(f'Request: {request.method} {request.path} from {request.remote_addr}')
    
    @app.after_request
    def log_response_info(response):
        """Log response information after processing."""
        if not request.path.startswith('/static/'):
            app.logger.debug(f'Response: {response.status} for {request.method} {request.path}')
        return response
        
    return app 