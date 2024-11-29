import sqlite3
from cryptography.fernet import Fernet

# Load the key used for encryption and decryption
def load_key():
    return open('secret.key', 'rb').read()

key = load_key()
cipher = Fernet(key)

# Decrypt the password
def decrypt_password(encrypted_password: str) -> str:
    return cipher.decrypt(encrypted_password.encode()).decode()

# Retrieve credentials from the database based on username and website
def retrieve_credentials(website: str, username: str):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT website, username, encrypted_password FROM credentials WHERE website=? AND username=?", (website, username))
    data = cursor.fetchone()
    conn.close()

    if data:
        decrypted_password = decrypt_password(data[2])
        print(f"Website: {data[0]}\nUsername: {data[1]}\nPassword: {decrypted_password}")
    else:
        print("No credentials found for the given website and username.")

if __name__ == "__main__":
    website_input = input("Enter Website: ")
    username_input = input("Enter Username: ")

    retrieve_credentials(website_input, username_input)
