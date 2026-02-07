import uuid
from datetime import datetime
from sqlmodel import Session, create_engine
from backend.models import User
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
        # Create a new user
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