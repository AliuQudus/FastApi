from pydantic import BaseModel, EmailStr, Field
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
    published: Optional[bool] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = {"from_attributes": True}


class Response(BaseModel):
    id: int
    username: str
    title: str
    content: str
    rating: Optional[float] = None
    published: Optional[bool] = None
    created_at: datetime
    owner: UserResponse

    model_config = {"from_attributes": True}


class Login(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class Likes(BaseModel):
    post_id: int
    dir: int = Field(..., ge=0, le=1)
