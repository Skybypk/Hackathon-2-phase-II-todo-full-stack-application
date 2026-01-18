from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from app.database.engine import engine
from app.models.user import User, UserCreate, UserRead
from app.core.security import get_password_hash, verify_password, create_access_token, get_current_user
from datetime import timedelta
from typing import Dict

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
    """Register a new user."""
    with Session(engine) as session:
        # Check if user already exists
        existing_user = session.exec(select(User).where(User.email == user.email)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        # Create new user
        db_user = User(
            email=user.email,
            password_hash=get_password_hash(user.password)
        )
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


@router.post("/login")
def login(email: str, password: str):
    """Authenticate user and return access token."""
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == email)).first()

        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token_expires = timedelta(minutes=30 * 24)  # 30 days
        access_token = create_access_token(
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email
            }
        }


@router.get("/me", response_model=UserRead)
def get_current_user_info(current_user_id: str = Depends(get_current_user)):
    """Get current user info."""
    with Session(engine) as session:
        user = session.get(User, current_user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user