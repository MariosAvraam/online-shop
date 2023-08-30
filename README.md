# eCommerce Flask Application

This repository contains a simple eCommerce web application built with Flask. Users can register, login, view products, add products to their cart, and checkout. Administrators have additional capabilities to add, edit, or delete products.

## Features
- User Registration and Login
- Admin User Management
- Product Display
- Add Products to Cart
- Admin Product Management (Add, Edit, Delete)

## Prerequisites
- Python 3.X

## Installation & Setup

### 1. Cloning the repository
To get started, you'll need to clone the repository to your local machine:
```bash
git clone https://github.com/MariosAvraam/online-shop.git
```
### 2. Navigate to the directory
```bash
cd online-shop
```

### 3. (Optional) Creating a Virtual Environment
It's a best practice to use a virtual environment to manage dependencies for your project. This step is optional but recommended:
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate

# On macOS and Linux:
source venv/bin/activate
```

### 4. Installing Dependencies
Once inside the project directory, you can install the necessary dependencies using pip:
```bash
pip install -r requirements.txt
```

### 5. Configuration & Customization
To modify the default admin email:

1. Navigate to `app.py`.
2. Locate the line:
```bash
if email == "example_email@email.com":
```
3. Change "example_email@email.com" to your desired admin email address.
This email address will have administrator privileges when registered, allowing for product management capabilities.

### 6. Running the Application
To run the application, simply execute:
```bash
python app.py
```
After executing the command, you should see output indicating that the server is running. The application will be available at `http://127.0.0.1:5000/` in your web browser.

## Usage
1. Start by registering a new user account or logging in if you already have one.
2. Browse through the list of products.
3. Add products to your cart.
4. Administrators can add new products, edit existing products, or delete products.

## Contributing
Pull requests are welcome. Please ensure your PRs are well-documented.

## License
This project is open-source. Feel free to use, modify, and distribute the code as you see fit.