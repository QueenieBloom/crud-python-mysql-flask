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

def connect(database=None):
    """Create a connection to the MySQL database. If database is None, connect without specifying a database."""
    # Decrypt database credentials
    db_credentials = decrypt_credentials("db_credentials.txt")

    return mysql.connector.connect(
        host=db_credentials[1],  # db_host
        user=db_credentials[2],  # db_user
        password=db_credentials[3],  # db_password
        database=database or db_credentials[0]  # db_name if specified, otherwise None
    )

def create_database():
    """Create the users_reg database if it doesn't exist."""
    db_credentials = decrypt_credentials("db_credentials.txt")
    db_name = db_credentials[0]

    try:
        conn = connect(database=None)  # Connect without specifying a database
        cursor = conn.cursor()
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {db_name}")
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Database '{db_name}' created successfully or already exists.")
    except Error as e:
        print("Error creating database:", e)

def create_table():
    """Create the users table if it doesn't exist within the users_reg database."""
    db_credentials = decrypt_credentials("db_credentials.txt")
    db_name = db_credentials[0]

    try:
        conn = connect(database=db_name)  # Connect to the specified database
        cursor = conn.cursor()
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS users (
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
    """Create the database and table if they don't exist."""
    create_database()  # Create the database
    create_table()     # Create the users table within the database

def insert_user(first_name, last_name, username, email, password):
    """Inserts a new user into the users table."""
    db_credentials = decrypt_credentials("db_credentials.txt")
    db_name = db_credentials[0]

    try:
        conn = connect(database=db_name)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (firstName, lastName, username, email, password)
            VALUES (%s, %s, %s, %s, %s)
        """, (first_name, last_name, username, email, password))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"User '{username}' inserted successfully.")
    except Error as e:
        print("Error inserting user:", e)