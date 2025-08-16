from pydoc import text
from tkinter import Text
from sqlalchemy import TIMESTAMP, Column, Integer, text, String, Boolean
from .database import Base


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    rating = Column(String, nullable=True)
    published = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
