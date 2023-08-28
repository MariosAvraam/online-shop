from flask_login import UserMixin
from database import db

class User(UserMixin, db.Model):
    """User model to store user data."""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    cart = db.relationship('Cart', backref='user')
