from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid


class UserBase(BaseModel):
    email: str


class UserRegister(UserBase):
    password: str


class UserLogin(UserBase):
    password: str


class UserResponse(UserBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class TokenData(BaseModel):
    user_id: Optional[str] = None