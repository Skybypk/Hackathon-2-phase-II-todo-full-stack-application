from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime, timedelta
from typing import Optional
import uuid
import hashlib
import hmac

try:
    from passlib.context import CryptContext
    from jose import JWTError, jwt

    try:
        # Try to initialize bcrypt
        pwd_context = CryptContext(
            schemes=["bcrypt", "pbkdf2_sha256"],
            deprecated="auto",
            bcrypt__ident="2b",
            bcrypt__rounds=10,
            pbkdf2_sha256__default_rounds=29000
        )
        HAS_BCRYPT = True
    except Exception:
        # If bcrypt fails to initialize, set flag to False
        HAS_BCRYPT = False
        pwd_context = None
except ImportError:
    # If passlib is not available, set flags appropriately
    HAS_BCRYPT = False
    pwd_context = None

try:
    from ..models import User, UserBase
    from ..db import get_session
    from ..auth import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user
    from ..schemas.auth import UserRegister, UserLogin, UserResponse, Token
except ImportError:
    from models import User, UserBase
    from db import get_session
    from auth import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user
    from schemas.auth import UserRegister, UserLogin, UserResponse, Token

router = APIRouter(prefix="/api/auth", tags=["auth"])


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash."""
    if HAS_BCRYPT:
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            # If bcrypt verification fails, try fallback
            return hashed_password == hashlib.sha256(plain_password.encode()).hexdigest()
    else:
        # Fallback verification using SHA256 (not secure, for development only)
        return hashed_password == hashlib.sha256(plain_password.encode()).hexdigest()


def get_password_hash(password: str) -> str:
    """Generate a hash for the given password."""
    if HAS_BCRYPT:
        try:
            # Bcrypt has a 72-byte password length limit
            # Truncate if necessary to avoid ValueError
            password_bytes = password.encode('utf-8')
            if len(password_bytes) > 72:
                # Truncate to 72 bytes and decode back to string
                password = password_bytes[:72].decode('utf-8', errors='ignore')
            return pwd_context.hash(password)
        except Exception:
            # If bcrypt hashing fails, fall back to SHA256
            return hashlib.sha256(password.encode()).hexdigest()
    else:
        # Fallback to SHA256 (not secure, for development only)
        return hashlib.sha256(password.encode()).hexdigest()


@router.post("/register", response_model=UserResponse)
def register_user(
    user_register: UserRegister,
    session: Session = Depends(get_session)
):
    """Register a new user with email and password"""
    try:
        # Check if user already exists
        existing_user = session.exec(
            select(User).where(User.email == user_register.email)
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        # Validate password strength (at least 8 digits)
        password = user_register.password

        # Check if password meets the 72-byte limit before validation
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            # Truncate to 72 bytes before validation to ensure consistency
            password = password_bytes[:72].decode('utf-8', errors='ignore')

        digit_count = sum(1 for c in password if c.isdigit())
        if digit_count < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least 8 digits"
            )

        # Create new user
        hashed_password = get_password_hash(password)
        user = User(
            email=user_register.email,
            password_hash=hashed_password
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        return UserResponse(
            id=user.id,
            email=user.email,
            created_at=user.created_at
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log the error for debugging
        print(f"Error in register_user: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        )


@router.post("/login", response_model=Token)
def login_user(
    user_login: UserLogin,
    session: Session = Depends(get_session)
):
    """Authenticate user with email and password"""
    user = session.exec(
        select(User).where(User.email == user_login.email)
    ).first()

    # Handle password truncation for consistency with registration
    password = user_login.password
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        # Truncate to 72 bytes for consistency with registration
        password = password_bytes[:72].decode('utf-8', errors='ignore')

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=user.id,
            email=user.email,
            created_at=user.created_at
        )
    )


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get current user's profile information"""
    try:
        user_uuid = uuid.UUID(current_user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    user = session.get(User, user_uuid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(
        id=user.id,
        email=user.email,
        created_at=user.created_at
    )


@router.post("/logout")
def logout_user():
    """End user session (client-side token removal is sufficient)"""
    return {"message": "Logged out successfully"}