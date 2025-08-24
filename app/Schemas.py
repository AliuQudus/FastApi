from pyclbr import Class
from pydantic import BaseModel, EmailStr
from typing import Optional


class createPost(BaseModel):
    username: str
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
