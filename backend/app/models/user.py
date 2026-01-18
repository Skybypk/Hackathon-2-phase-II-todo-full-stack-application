from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)


class User(UserBase, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password_hash: str = Field(nullable=False, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserRead(SQLModel):
    id: uuid.UUID
    email: str
    created_at: datetime


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    email: Optional[str] = None