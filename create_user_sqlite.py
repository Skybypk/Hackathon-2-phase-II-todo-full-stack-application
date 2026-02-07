import sqlite3
import hashlib
import uuid
from datetime import datetime

# Directly insert a user into the SQLite database
db_path = 'D:/Quarter-4/Projects/Q4-Hackathon-02/h-2/backend/todo_app.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create a simple hashed password using SHA256 (just for testing purposes)
# In a real application, we'd use bcrypt, but since it's causing issues
password = "AdminPass12345678!"
# For testing, we'll use a simple hash (not secure, but will work for testing)
hashed_password = hashlib.sha256(password.encode()).hexdigest()

user_id = str(uuid.uuid4())
email = "admin@example.com"

try:
    cursor.execute("""
        INSERT INTO users (id, email, password_hash, created_at, updated_at) 
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id, 
        email, 
        hashed_password, 
        datetime.now(), 
        datetime.now()
    ))
    
    conn.commit()
    print(f'Default user created successfully!')
    print(f'Email: {email}')
    print(f'Password: {password}')
    print('You can now use these credentials to log in.')
    
except sqlite3.IntegrityError:
    print(f'Default user already exists with email: {email}')
    
except Exception as e:
    print(f'Error creating default user: {e}')
    
finally:
    conn.close()