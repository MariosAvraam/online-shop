from flask_login import UserMixin
from database import db

class User(UserMixin, db.Model):
    """
    User model to store user data.
    
    Attributes:
        id (int): Unique identifier for each user.
        email (str): Email address of the user.
        password (str): Hashed password of the user.
        name (str): Name of the user.
        is_admin (bool): Flag to indicate if the user is an admin.
        cart (relationship): Relationship to the Cart model.
    """
    
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    cart = db.relationship('Cart', backref='user')
