# website/models.py
import mysql.connector
from mysql.connector import Error
from cryptography.fernet import Fernet
import os

def decrypt_credentials(filename):
    """Decrypt credentials stored in a specified file."""
    # Load crypto key from environment variable
    crypto_key = os.getenv("CRYPTO_KEY")
    cipher_suite = Fernet(crypto_key)

    with open(filename, "rb") as file:
        encrypted_credentials = file.readlines()
        decrypted_credentials = [cipher_suite.decrypt(line.strip()).decode() for line in encrypted_credentials]
    
    return decrypted_credentials

def connect():
    """Create a connection to the MySQL database."""
    # Decrypt database credentials
    db_credentials = decrypt_credentials("db_credentials.txt")

    return mysql.connector.connect(
        host=db_credentials[1],  # db_host
        user=db_credentials[2],  # db_user
        password=db_credentials[3],  # db_password
        # NOTE: We're not specifying a database here initially
    )

def create_database():
    """Create the database if it doesn't exist."""
    db_credentials = decrypt_credentials("db_credentials.txt")
    
    try:
        conn = mysql.connector.connect(
            host=db_credentials[1],  # db_host
            user=db_credentials[2],  # db_user
            password=db_credentials[3],  # db_password
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_credentials[0]}")  # db_name
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Database '{db_credentials[0]}' created successfully or already exists.")
    except Error as e:
        print("Error creating database:", e)

def create_schema():
    """Create the user_regis schema if it doesn't exist."""
    db_credentials = decrypt_credentials("db_credentials.txt")
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS user_regis")
        conn.commit()
        cursor.close()
        conn.close()
        print("Schema 'user_regis' created successfully or already exists.")
    except Error as e:
        print("Error creating schema:", e)

def create_table():
    """Create the users table if it doesn't exist."""
    db_credentials = decrypt_credentials("db_credentials.txt")
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS user_regis.users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            firstName VARCHAR(50) NOT NULL,
            lastName VARCHAR(50) NOT NULL,
            username VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Table 'users' created successfully or already exists.")
    except Error as e:
        print("Error creating table:", e)

def create_database_and_table():
    """Create the database, schema, and table if they don't exist."""
    create_database()  # Create the database
    create_schema()    # Create the user_regis schema
    create_table()     # Create the users table within the schema
