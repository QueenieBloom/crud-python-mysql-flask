import secrets
from cryptography.fernet import Fernet

# Generating a random key of 32 characters
secret_key = secrets.token_hex(16)
print(f'Your generated SECRET_KEY is: {secret_key}')

# Generating an encryption key
key = Fernet.generate_key()
print("Encryption key:", key.decode())
