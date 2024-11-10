from cryptography.fernet import Fernet

# Generate a key (store this securely)
key = Fernet.generate_key()

# Initialize a cipher suite
cipher = Fernet(key)

# Encrypt the password
password = "fuckitweball"
encrypted_password = cipher.encrypt(password.encode())

print(f"Encrypted password: {encrypted_password}")

# Decrypt the password (just to show how to decrypt it)
decrypted_password = cipher.decrypt(encrypted_password).decode()

print(f"Decrypted password: {decrypted_password}")
