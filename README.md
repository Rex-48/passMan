# Secure Password Manager

This is a simple password manager application built using Python. It allows users to securely store and retrieve credentials such as website usernames and passwords. The application uses encryption to store passwords safely, and SQLite to manage the credential database. The app is designed with a master password that must be entered to access the password manager interface.

## Features

- **Secure Encryption**: User passwords are encrypted using the `cryptography.fernet` symmetric encryption algorithm.
- **Database Storage**: Passwords and credentials are stored in an SQLite database, ensuring data persistence across sessions.
- **Simple User Interface**: A user-friendly GUI built using `Tkinter` allows easy interaction.
- **Master Password**: A master password is required to access the password manager interface, ensuring only authorized users can manage credentials.
  
## Requirements

To run this project, you'll need the following libraries:

- `sqlite3` (for database functionality)
- `cryptography` (for password encryption and decryption)
- `tkinter` (for creating the GUI)
  
Install the required libraries using `pip`:

```bash
pip install cryptography
