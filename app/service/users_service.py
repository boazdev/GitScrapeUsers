from sqlalchemy.orm import Session
#from sqlalchemy import select, join
from typing import Optional
from app.models.user_model import User
from app.schemas import user_schema
from sqlalchemy.exc import IntegrityError
def get_user_by_username(db: Session, username: str) -> User: 
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, id: str):
    return db.query(User).filter(User.id == id).first()

def create_user(db: Session, user: user_schema.UserCreate) -> Optional[user_schema.User]:
    try:
        db_user = User(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e: #duplicate username 
        return None

