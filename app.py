from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return "Welcome to our eCommerce site!"

if __name__ == "__main__":
    app.run(debug=True)
