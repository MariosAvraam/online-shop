from database import db

class Cart(db.Model):
    """Cart model to store cart data."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', back_populates='cart_items')
    quantity = db.Column(db.Integer, default=1, nullable=False)
