from database import db

class Product(db.Model):
    """Product model to store product data."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(300), nullable=True)
    cart_items = db.relationship('Cart', back_populates='product', cascade='all, delete-orphan')
