import sqlite3
from cryptography.fernet import Fernet
import hashlib
import tkinter as tk
from tkinter import messagebox, simpledialog

# Key generation and loading
def generate_key():
    return Fernet.generate_key()

def load_key():
    try:
        return open('secret.key', 'rb').read()
    except FileNotFoundError:
        key = generate_key()
        with open('secret.key', 'wb') as key_file:
            key_file.write(key)
        return key

key = load_key()
cipher = Fernet(key)

# Encryption and decryption functions
def encrypt_password(password: str) -> str:
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password: str) -> str:
    return cipher.decrypt(encrypted_password.encode()).decode()

# Database initialization
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS credentials
                     (id INTEGER PRIMARY KEY, website TEXT, username TEXT, encrypted_password TEXT)''')
    conn.commit()
    conn.close()

# Master password setup
MASTER_PASSWORD = "15664316x"  # Replace with a secure master password

def verify_master_password(input_password: str) -> bool:
    hashed_password = hashlib.sha256(input_password.encode()).hexdigest()
    return hashed_password == hashlib.sha256(MASTER_PASSWORD.encode()).hexdigest()

# Add credential to database
def add_credential(website, username, password):
    if not website or not username or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    encrypted_password = encrypt_password(password)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO credentials (website, username, encrypted_password) VALUES (?, ?, ?)", 
                   (website, username, encrypted_password))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Credential added successfully!")
    clear_entries()

# Clear input fields
def clear_entries():
    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

# GUI setup
def main_app():
    global website_entry, username_entry, password_entry

    root = tk.Tk()
    root.title("Secure Password Manager")
    root.geometry("400x250")
    root.resizable(False, False)

    form_frame = tk.Frame(root, padx=10, pady=10)
    form_frame.pack(fill=tk.X)

    tk.Label(form_frame, text="Website:", font=("Arial", 12)).grid(row=0, column=0, sticky=tk.W, pady=5)
    tk.Label(form_frame, text="Username:", font=("Arial", 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
    tk.Label(form_frame, text="Password:", font=("Arial", 12)).grid(row=2, column=0, sticky=tk.W, pady=5)

    website_entry = tk.Entry(form_frame, width=40)
    username_entry = tk.Entry(form_frame, width=40)
    password_entry = tk.Entry(form_frame, width=40, show="*")

    website_entry.grid(row=0, column=1, padx=5, pady=5)
    username_entry.grid(row=1, column=1, padx=5, pady=5)
    password_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Button(form_frame, text="Add Credential", command=lambda: add_credential(website_entry.get(), username_entry.get(), password_entry.get()), 
              bg="green", fg="white", font=("Arial", 12)).grid(row=3, columnspan=2, pady=10)

    root.mainloop()

# Initialize database
init_db()

# Run the app if the master password is correct
if verify_master_password(simpledialog.askstring("Master Password", "Enter Master Password:", show="*")):
    main_app()
else:
    messagebox.showerror("Error", "Invalid Master Password!")
