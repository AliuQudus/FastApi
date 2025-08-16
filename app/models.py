from sqlalchemy import Column, Integer, String, Boolean
from .database import Base


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, nullable=False)
    username = Column(String, nullable=False, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    rating = Column(String, nullable=True)
    published = Column(Boolean, default=True)
