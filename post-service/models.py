# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from db import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    content = Column(String(280), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
