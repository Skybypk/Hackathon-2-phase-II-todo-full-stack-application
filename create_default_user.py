import uuid
from datetime import datetime
import hashlib
import sqlite3
import sys
import os

# Add the backend directory to the Python path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from passlib.context import CryptContext

# Configure password hashing context with the same settings as in auth.py
pwd_context = CryptContext(
    schemes=["bcrypt", "pbkdf2_sha256"],
    deprecated="auto",
    bcrypt__ident="2b",
    bcrypt__rounds=10,
    pbkdf2_sha256__default_rounds=29000
)

def get_password_hash(password: str) -> str:
    """Generate a hash for the given password."""
    # Bcrypt has a 72-byte password length limit
    # Truncate if necessary to avoid ValueError
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        # Truncate to 72 bytes and decode back to string
        password = password_bytes[:72].decode('utf-8', errors='ignore')
    return pwd_context.hash(password)

# Connect to the database
db_path = 'D:/Quarter-4/Projects/Q4-Hackathon-02/h-2/backend/todo_app.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create a default user
default_email = "admin@example.com"
default_password = "AdminPass123!"

# Hash the password using the same method as the auth system
hashed_password = get_password_hash(default_password)

# Generate a UUID for the user
user_id = str(uuid.uuid4())

# Insert the user into the database
try:
    cursor.execute("""
        INSERT INTO users (id, email, password_hash, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        default_email,
        hashed_password,
        datetime.now(),
        datetime.now()
    ))

    conn.commit()
    print(f"Default user created successfully!")
    print(f"Email: {default_email}")
    print(f"Password: {default_password}")
    print("You can now use these credentials to log in.")

except sqlite3.IntegrityError:
    print(f"Default user already exists with email: {default_email}")

except Exception as e:
    print(f"Error creating default user: {e}")

finally:
    conn.close()