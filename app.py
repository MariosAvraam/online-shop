from flask import Flask
from database import db
import models


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "Welcome to our eCommerce site!"

if __name__ == "__main__":
    app.run(debug=True)
