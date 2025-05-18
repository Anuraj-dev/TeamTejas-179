from .base import BaseModel, db

class Purchase(BaseModel):
    __tablename__ = 'purchases'

    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='completed')
    
    # Purchase items
    items = db.relationship('PurchaseItem', backref='purchase', lazy='dynamic',
                          cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Purchase {self.id} by User {self.buyer_id}>'

class PurchaseItem(BaseModel):
    __tablename__ = 'purchase_items'

    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchases.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price_at_purchase = db.Column(db.Numeric(10, 2), nullable=False)  # Historical price

    def __repr__(self):
        return f'<PurchaseItem {self.product_id} in Purchase {self.purchase_id}>'
