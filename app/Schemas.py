from pyclbr import Class
from pydantic import BaseModel
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
