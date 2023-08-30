from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models.user import User
from models.cart import Cart
from models.product import Product
from forms import RegisterForm, LoginForm, ProductForm, EditProductForm
from functools import wraps

app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'  # SQLite Database URL
app.config['SECRET_KEY'] = 'Secret123'  # Secret key for session management

# Initializing bootstrap for the app
Bootstrap5(app)

# Initializing the database for the app
db.init_app(app)

# Setting up the login manager for user authentication
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    """
    Load the user with the provided user_id.
    
    :param user_id: User's ID
    :return: User object
    """
    return User.query.get(int(user_id))

# Create all database tables within the application context
with app.app_context():
    db.create_all()

def admin_required(func):
    """
    Decorator function to ensure the user is an admin.
    
    :param func: Function to be decorated
    :return: Wrapped function
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return login_manager.unauthorized()
        elif not current_user.is_admin:
            return flash("You're not authorized to view this page"), 403
        return func(*args, **kwargs)
    return decorated_view

@app.route('/')
def index():
    """Home route. Displays welcome page with options to register or login."""
    if current_user.is_authenticated:
        return redirect(url_for('display_products'))
    return render_template('index.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    """
    User registration route. Handles both the display of the registration form
    and the submission of registration details.
    """
    form = RegisterForm()
    
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()

        # Check if email already exists
        if user:
            flash("You've already signed up with this email, login instead.", "success")
            return redirect(url_for('login'))

        # Hash the password
        hashed_password = generate_password_hash(
            form.password.data, method='pbkdf2:sha256', salt_length=8)
        new_user = User(
            email=email,
            name=form.name.data,
            password=hashed_password,
        )

        # Check if the user should be an admin (based on email)
        if email == "example_email@email.com":
            new_user.is_admin = True

        # Add new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Log the user in
        login_user(new_user)
        flash("Registered successfully!", "success")
        return redirect(url_for('display_products'))
    
    return render_template("register.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """
    User login route. Handles both the display of the login form
    and the submission of login details.
    """
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        password = form.password.data
        
        # Check if user exists and password is correct
        if not user:
            flash("Email does not exist. Please try again.", "success")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash("Password incorrect. Please try again.", "success")
            return redirect(url_for('login'))
        
        # Log the user in
        login_user(user)
        flash("Logged in successfully!", "success")
        return redirect(url_for('display_products'))
    
    return render_template("login.html", form=form)

@app.route('/logout')
@login_required
def logout():
    """Route to handle user logout."""
    logout_user()
    flash("Logged out successfully!", "success")
    return redirect(url_for('index'))

@app.route('/products')
def display_products():
    """Route to display all available products."""
    all_products = Product.query.all()
    return render_template('products.html', all_products=all_products)

@app.route('/products/<int:product_id>')
def product_detail(product_id):
    """Route to display the details of a single product."""
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    """
    Route to add a new product. Only accessible by admins.
    Handles both the display of the form and the submission.
    """
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            image_url=form.image_url.data
        )

        # Add the product to the database
        db.session.add(new_product)
        db.session.commit()
        flash("Product added successfully!", "success")
        return redirect(url_for('display_products'))
    
    return render_template('add_product.html', form=form)

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    """
    Route to edit an existing product. Only accessible by admins.
    Handles both the display of the form and the submission.
    """
    product = Product.query.get_or_404(product_id)
    form = EditProductForm(obj=product)
    
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.image_url = form.image_url.data

        db.session.commit()
        flash("Product updated successfully!", "success")
        return redirect(url_for('display_products'))

    return render_template('edit_product.html', form=form, product=product)

@app.route('/delete_product/<int:product_id>', methods=['POST'])
@login_required
@admin_required
def delete_product(product_id):
    """
    Route to delete a product. Only accessible by admins.
    """
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully!", "success")
    return redirect(url_for('display_products'))

@app.route('/cart')
@login_required
def view_cart():
    """
    Route to display the current user's cart.
    Displays all items in the cart and the total price.
    """
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    total = sum([item.product.price * item.quantity for item in cart_items])
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    """
    Route to add a product to the user's cart.
    If the product is already in the cart, increments the quantity.
    """
    product = Product.query.get_or_404(product_id)
    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = Cart(user_id=current_user.id, product_id=product_id)
        db.session.add(cart_item)
    
    db.session.commit()
    flash(f"{product.name} added to cart!", "success")
    return redirect(url_for('display_products'))

if __name__ == "__main__":
    # Running the app in debug mode
    app.run(debug=True)
