from .base import BaseModel, db

class Cart(BaseModel):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # Cart items
    items = db.relationship('CartItem', backref='cart', lazy='dynamic',
                          cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Cart for User {self.user_id}>'

class CartItem(BaseModel):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f'<CartItem {self.product_id} in Cart {self.cart_id}>'
