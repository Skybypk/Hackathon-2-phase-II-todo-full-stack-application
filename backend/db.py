from sqlmodel import create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL from environment variable
NEON_DB_URL = os.getenv("NEON_DB_URL")
if not NEON_DB_URL:
    # Fallback to local SQLite for development
    DATABASE_URL = "sqlite:///./todo_app.db"
else:
    DATABASE_URL = NEON_DB_URL

# Create database engine
engine = create_engine(DATABASE_URL, echo=False)


def get_session():
    with Session(engine) as session:
        yield session