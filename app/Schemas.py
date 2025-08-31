"""
from pydantic import BaseModel, EmailStr
from typing import Optional


class createPost(BaseModel):
    title: str
    content: str
    rating: Optional[float] = None
    published: Optional[bool] = None


class UpdatePost(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    rating: Optional[float] = None


class Response(BaseModel):
    title: str
    content: str
    rating: Optional[float] = None
    published: Optional[bool] = None

    model_config = {"from_attributes": True}  # allows SQLAlchemy objects


class Login(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    username: str
    email: EmailStr

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class createPost(BaseModel):
    title: str
    content: str
    rating: Optional[float] = None
    published: Optional[bool] = None


class UpdatePost(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    rating: Optional[float] = None
    published: Optional[bool] = (
        None  # Added this in case user wants to update publish status
    )


class Response(BaseModel):
    id: int  # Added ID field for unique identification
    username: str  # Added username to show who created the post
    title: str
    content: str
    rating: Optional[float] = None
    published: Optional[bool] = None
    created_at: datetime  # Added timestamp

    model_config = {"from_attributes": True}  # allows SQLAlchemy objects


class Login(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int  # Added ID field
    username: str
    email: EmailStr
    created_at: datetime  # Added timestamp

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
