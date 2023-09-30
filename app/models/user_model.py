from sqlalchemy import  Column, Integer, String
from app.database.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer,autoincrement=True, primary_key=True, index=True)
    username = Column(String, unique=True)