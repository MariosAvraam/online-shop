from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models.user import User
from models.cart import Cart
from models.order import Order
from models.product import Product
from forms import RegisterForm, LoginForm, ProductForm
from functools import wraps

app = Flask(__name__)

# Configurations for the database and secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SECRET_KEY'] = 'Secret123'

# Initializing bootstrap for the app
Bootstrap5(app)

# Initializing the database for the app
db.init_app(app)

# Setting up the login manager for user authentication
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    """Load the user with the provided user_id."""
    return db.get_or_404(User, user_id)

with app.app_context():
    # Create all database tables
    db.create_all()
    
    # Check if there are any products, if not, add some sample products
    if Product.query.count() == 0:
        sample_products = [
            Product(name="Sample Product 1", description="This is a sample product.", price=19.99, image_url="https://via.placeholder.com/150"),
            Product(name="Sample Product 2", description="This is another sample product.", price=29.99, image_url="https://via.placeholder.com/150"),
        ]
        db.session.add_all(sample_products)
        db.session.commit()

def admin_required(func):
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
    """Home route - Welcome page with options to register or login."""
    return render_template('index.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    """User registration route."""
    form = RegisterForm()
    
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()

        if user:
            flash("You've already signed up with this email, login instead.")
            return redirect(url_for('login'))

        hashed_password = generate_password_hash(
            form.password.data, method='pbkdf2:sha256', salt_length=8)
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hashed_password,
        )

        if email == "ma@gmail.com":
            new_user.is_admin = True

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template("register.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """User login route."""
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        password = form.password.data
        
        if not user:
            flash("Email does not exist. Please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash("Password incorrect. Please try again.")
            return redirect(url_for('login'))
        
        login_user(user)
        return redirect(url_for('index'))
    return render_template("login.html", form=form)

@app.route('/logout')
@login_required
def logout():
    """Route to log out the user."""
    logout_user()
    flash("Logged out successfully!", "success")
    return redirect(url_for('index'))

@app.route('/products')
def display_products():
    """Route to display all products."""
    all_products = Product.query.all()
    return render_template('products.html', all_products=all_products)

@app.route('/products/<int:product_id>')
def product_detail(product_id):
    """Route to display a single product detail."""
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            image_url=form.image_url.data
        )
        db.session.add(new_product)
        db.session.commit()
        flash("Product added successfully!", "success")
        return redirect(url_for('display_products'))
    return render_template('add_product.html', form=form)


@app.route('/cart')
@login_required
def view_cart():
    """Route to view the user's cart."""
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    total = sum([item.product.price * item.quantity for item in cart_items])
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    """Route to add a product to the user's cart."""
    product = Product.query.get_or_404(product_id)
    
    # Check if the product is already in the cart
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
    app.run(debug=True)
