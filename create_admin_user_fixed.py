import uuid
from datetime import datetime
from sqlmodel import Session, create_engine
from backend.models import User

# Create the database engine
DATABASE_URL = "sqlite:///./todo_app.db"
engine = create_engine(DATABASE_URL)

# Create a user directly in the database
with Session(engine) as session:
    # Check if user already exists
    from sqlalchemy import select
    existing_user = session.exec(select(User).where(User.email == "admin@example.com")).first()

    if existing_user:
        print("Admin user already exists")
    else:
        # Import the password hashing function from the routes module
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
        
        from routes.auth import get_password_hash

        user_id = uuid.uuid4()
        hashed_password = get_password_hash("AdminPass12345678!")

        user = User(
            id=user_id,
            email="admin@example.com",
            password_hash=hashed_password
        )

        session.add(user)
        session.commit()
        print("Admin user created successfully!")
        print(f"Email: admin@example.com")
        print(f"Password: AdminPass12345678!")