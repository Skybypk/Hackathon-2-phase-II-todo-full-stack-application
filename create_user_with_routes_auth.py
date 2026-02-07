import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from sqlmodel import Session, select
from backend.db import engine
from backend.models import User
from backend.routes.auth import get_password_hash
import uuid

# Create a user directly in the database using the proper backend functions
with Session(engine) as session:
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == "admin@example.com")).first()

    if existing_user:
        print("Admin user already exists")
    else:
        # Create a new user
        user_id = uuid.uuid4()
        # Use a shorter password to avoid bcrypt issues
        password = "Pass1234!"
        print(f"Hashing password: {password}")
        hashed_password = get_password_hash(password)

        user = User(
            id=user_id,
            email="admin@example.com",
            password_hash=hashed_password
        )

        session.add(user)
        session.commit()
        print("Admin user created successfully!")
        print(f"Email: admin@example.com")
        print(f"Password: {password}")