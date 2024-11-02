# website/__init__.py
from flask import Flask
from dotenv import load_dotenv
import os
from .models import create_database_and_table  # Import the new function
from cryptography.fernet import Fernet
from .views import views
from .auth import auth

load_dotenv()

def decrypt_credentials(file_path):
    """Decrypt credentials from the specified file."""
    crypto_key = os.getenv("CRYPTO_KEY")
    cipher_suite = Fernet(crypto_key)
    
    with open(file_path, "rb") as file:
        lines = file.readlines()
        return [cipher_suite.decrypt(line.strip()).decode() for line in lines]

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    
    # Decrypt admin and database credentials
    admin_username, admin_password = decrypt_credentials("admin_credentials.txt")
    db_name, db_host, db_user, db_password = decrypt_credentials("db_credentials.txt")

    # Set admin and database credentials
    app.config['ADMIN_USERNAME'] = admin_username
    app.config['ADMIN_PASSWORD'] = admin_password
    app.config['DB_NAME'] = db_name
    app.config['DB_HOST'] = db_host
    app.config['DB_USER'] = db_user
    app.config['DB_PASSWORD'] = db_password

    # Create the schema and table
    create_database_and_table()  # Update to create schema and table
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    return app
