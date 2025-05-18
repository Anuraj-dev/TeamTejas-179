import os
from datetime import timedelta

class Config:
    """Base config."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-please-change-in-production')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join('app', 'static', 'images', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Security settings
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_SECURE = False
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = timedelta(days=14)
    
    # CSRF settings
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hour
    
    # Mail settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@ecofinds.com')
    
    # Rate limiting settings
    RATELIMIT_STORAGE_URL = 'memory://'
    RATELIMIT_STRATEGY = 'fixed-window'
    RATELIMIT_HEADERS_ENABLED = True

class DevelopmentConfig(Config):
    """Development config."""
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI', 'sqlite:///dev.db')
    # Disable strict security in development
    REQUIRE_HTTPS = False

class TestingConfig(Config):
    """Testing config."""
    FLASK_ENV = 'testing'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI', 'sqlite:///test.db')
    WTF_CSRF_ENABLED = False
    REQUIRE_HTTPS = False
    # Disable rate limiting for tests
    RATELIMIT_ENABLED = False

class ProductionConfig(Config):
    """Production config."""
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    # Enable strict security in production
    REQUIRE_HTTPS = True
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    # Set a strong secret key through environment variables
    SECRET_KEY = os.environ.get('SECRET_KEY')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
