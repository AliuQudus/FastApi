from pydoc import text

# from tkinter import CASCADE
from sqlalchemy import TIMESTAMP, Column, Integer, text, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String, ForeignKey("users.username"), nullable=False)
    """
    username = Column(
        String, ForeignKey("users.username", ondelete="CASCADE"), nullable=False
    )
    """
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    rating = Column(String, nullable=True)
    published = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    owner = relationship("Login", back_populates="posts")


class Login(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    posts = relationship("Post", back_populates="owner")


class Like(Base):
    __tablename__ = "likes"

    post_id = Column(
        Integer,
        ForeignKey("post.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    user_username = Column(
        String,
        ForeignKey("users.username", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
