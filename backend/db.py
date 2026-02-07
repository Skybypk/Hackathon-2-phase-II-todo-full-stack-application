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

# Create database engine with optimized settings for better performance
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,  # Verify connections before using them
    pool_recycle=300,    # Recycle connections every 5 minutes
    pool_size=10,        # Number of connection pools
    max_overflow=20      # Maximum number of connections beyond pool_size
)


def ensure_tables_exist():
    """Function to ensure database tables exist, called when needed"""
    from sqlmodel import SQLModel
    try:
        SQLModel.metadata.create_all(bind=engine)
        print("Database tables ensured to exist")
    except Exception as e:
        print(f"Error creating tables: {e}")


# Don't call this function automatically to avoid startup issues
# Tables will be created when first needed


def get_session():
    with Session(engine) as session:
        yield session