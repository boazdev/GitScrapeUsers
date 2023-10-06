from sqlalchemy import  Column, Integer, String
from app.database.db import Base


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String)