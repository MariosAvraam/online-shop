from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Email, Optional, URL

class RegisterForm(FlaskForm):
    """Form for user registration."""
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    """Form for user login."""
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class ProductForm(FlaskForm):
    """Form for adding a new product."""
    
    name = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    price = FloatField('Price', validators=[DataRequired()])
    image_url = StringField('Image URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Add Product')

class EditProductForm(FlaskForm):
    """Form for editing an existing product."""
    
    name = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    price = FloatField('Price', validators=[DataRequired()])
    image_url = StringField('Image URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Update Product')
