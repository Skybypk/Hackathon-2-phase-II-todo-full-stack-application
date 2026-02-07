import sqlite3

# Connect to the database
conn = sqlite3.connect('todo_app.db')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(f'Tables in database: {tables}')

for table_name, in tables:
    if table_name != 'sqlite_sequence':
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cursor.fetchone()[0]
        print(f"Table '{table_name}' has {count} records")

conn.close()