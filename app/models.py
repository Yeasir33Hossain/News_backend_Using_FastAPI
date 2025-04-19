# app/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from .database import Base

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    url = Column(String, nullable=False)
    publishedAt = Column(DateTime, nullable=False)
