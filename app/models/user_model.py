import datetime
from sqlalchemy import  Column, DateTime, Integer, String, func, Boolean
from app.database.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer,autoincrement=True, primary_key=True, index=True)
    username = Column(String, unique=True)
    is_outlaw = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=datetime.datetime(1970, 1, 1))
    #updated_at = Column(DateTime, default=func.now())