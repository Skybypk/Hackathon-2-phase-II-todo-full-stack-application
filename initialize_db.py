from backend.db import engine
from backend.models import SQLModel
from sqlmodel import SQLModel

print("Creating database tables...")
try:
    SQLModel.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
except Exception as e:
    print(f"Error creating database tables: {e}")