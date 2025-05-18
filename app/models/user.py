from .base import BaseModel, db
from app.extensions import bcrypt

class User(BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    profile_image = db.Column(db.String(255))  # URL/path to profile image
    
    # User's product listings
    listings = db.relationship('Product', backref='seller', lazy='dynamic',
                             foreign_keys='Product.seller_id')
    
    # User's cart
    cart = db.relationship('Cart', backref='user', uselist=False, 
                          cascade='all, delete-orphan')
    
    # User's purchase history
    purchases = db.relationship('Purchase', backref='buyer', lazy='dynamic')

    def __init__(self, username, email, password, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.email = email.lower()
        self.password = password  # This calls the password setter

    @property
    def password(self):
        """Prevent password from being accessed."""
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        """Set password to a hashed password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        """Check if provided password matches stored hash."""
        return bcrypt.check_password_hash(self.password_hash, password)
        
    @property
    def is_active(self):
        """Return True if user is active."""
        return True
        
    @property
    def is_authenticated(self):
        """Return True if user is authenticated."""
        return True
        
    @property
    def is_anonymous(self):
        """Return False as registered users are not anonymous."""
        return False
        
    def get_id(self):
        """Return the user ID as a unicode string."""
        return str(self.id)

    def __repr__(self):
        return f'<User {self.username}>'
