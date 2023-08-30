from database import db

class Cart(db.Model):
    """
    Cart model to store cart data for each user.
    
    Attributes:
        id (int): Unique identifier for each cart entry.
        user_id (int): ID of the user to whom the cart entry belongs.
        product_id (int): ID of the product in the cart entry.
        product (relationship): Relationship to the Product model.
        quantity (int): Number of units of the product in the cart.
    """
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', back_populates='cart_items')
    quantity = db.Column(db.Integer, default=1, nullable=False)
