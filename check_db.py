import sqlite3
import os

# Connect to the database
db_path = 'D:/Quarter-4/Projects/Q4-Hackathon-02/h-2/backend/todo_app.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Checking database tables...")

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(f"Tables in database: {tables}")

for table_name, in tables:
    if table_name != 'sqlite_sequence':
        # Count records in each table
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cursor.fetchone()[0]
        print(f"Table '{table_name}' has {count} records")
        
        # If it's the users table, show some details
        if table_name == 'users':
            cursor.execute("SELECT * FROM users LIMIT 10;")
            users = cursor.fetchall()
            print(f"Sample user data: {users}")
            
            # Show column info
            cursor.execute("PRAGMA table_info(users);")
            columns = cursor.fetchall()
            print("User table structure:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")

conn.close()
print("Database check complete.")