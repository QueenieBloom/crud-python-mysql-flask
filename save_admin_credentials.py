# save_admin_credentials.py
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
crypto_key = os.getenv("CRYPTO_KEY")
cipher_suite = Fernet(crypto_key)

# Administrator information
admin_username = "admin_user"
admin_password = "admin_password"

# Database information
db_name = "your_database_name"
db_host = "localhost"
db_user = "db_user"
db_password = "db_password"

# Encrypt administrator credentials
encrypted_admin_username = cipher_suite.encrypt(admin_username.encode())
encrypted_admin_password = cipher_suite.encrypt(admin_password.encode())

# Encrypt database credentials
encrypted_db_name = cipher_suite.encrypt(db_name.encode())
encrypted_db_host = cipher_suite.encrypt(db_host.encode())
encrypted_db_user = cipher_suite.encrypt(db_user.encode())
encrypted_db_password = cipher_suite.encrypt(db_password.encode())

# Save administrator credentials in admin_credentials.txt
with open("admin_credentials.txt", "wb") as file:
    file.write(encrypted_admin_username + b"\n" + encrypted_admin_password)

# Save database credentials in db_credentials.txt
with open("db_credentials.txt", "wb") as file:
    file.write(encrypted_db_name + b"\n")
    file.write(encrypted_db_host + b"\n")
    file.write(encrypted_db_user + b"\n")
    file.write(encrypted_db_password)

print("Credentials encrypted and saved successfully!")
