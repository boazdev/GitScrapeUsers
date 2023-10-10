from sqlalchemy.orm import Session
from sqlalchemy import func,text #select, join
from typing import Optional
from app.models.user_model import User
from app.schemas import user_schema
from sqlalchemy.exc import IntegrityError

def get_users(db: Session, skip: int = 0, limit: int = 100)->list[User]:
    return db.query(User).offset(skip).limit(limit).all()

def get_users_by_id_greater_than(db: Session, id: int, skip: int = 0, limit: int = 100)-> list[User]:
    query = db.query(User).filter(User.id >= id)
    query = query.offset(skip).limit(limit)
    users = query.all()
    return users

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
        db.rollback()
        return None

def create_users_from_lst(db:Session, user_lst : list[str])->int:
    num_users_added=0
    for user_str in user_lst:
        try:
            db_user_data = {
                'username': user_str  
            }
            db_user = User(**db_user_data)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            num_users_added+=1
        except IntegrityError as e: #duplicate username 
            db.rollback()
            print(f"error adding user , user already exists: {user_str}")
        except Exception as e:
            db.rollback()
            print(f"error adding user {user_str}: {e.__str__()}")
    return num_users_added

def get_num_users(db:Session):
    try:
        row_count = db.query(func.count(User.id)).scalar()
        return row_count
    except Exception as e:
        print(f"Error: {e}")
        return -1
    
def delete_all(db:Session):
    try:
        db.query(User).delete()
        reset_cmd = text("ALTER SEQUENCE users_id_seq RESTART WITH 1;")
        db.execute(reset_cmd)
        db.commit()
        return "deleted"
    except Exception as e:
        print(f"delete error: {e.__str__()}")
        return None
