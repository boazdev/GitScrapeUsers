from sqlalchemy import  Column, DateTime, Integer, String, func
from app.database.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer,autoincrement=True, primary_key=True, index=True)
    username = Column(String, unique=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())