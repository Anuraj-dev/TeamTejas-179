from .base import BaseModel, db

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

    def __repr__(self):
        return f'<User {self.username}>'
