from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models.product import Product
from forms import RegisterForm, LoginForm


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SECRET_KEY'] = 'Secret123'

Bootstrap5(app)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()
    # Check if there are any products, if not, add some sample products
    if Product.query.count() == 0:
        sample_products = [
            Product(name="Sample Product 1", description="This is a sample product.", price=19.99, image_url="https://via.placeholder.com/150"),
            Product(name="Sample Product 2", description="This is another sample product.", price=29.99, image_url="https://via.placeholder.com/150"),
        ]
        db.session.add_all(sample_products)
        db.session.commit()

@app.route('/')
def index():
    return "Welcome to our eCommerce site!"

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

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
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template("register.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        result = db.session.execute(
            db.select(User).where(User.email == form.email.data))
        user = result.scalar()
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

@app.route('/products')
def display_products():
    result = db.session.execute(db.select(Product))
    all_products = result.scalars()
    return render_template('products.html', all_products=all_products)

@app.route('/products/<int:product_id>')
def product_detail(product_id):
    product = db.get_or_404(Product, product_id)
    return render_template('product_detail.html', product=product)

if __name__ == "__main__":
    app.run(debug=True)
