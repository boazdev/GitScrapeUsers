import datetime
from psycopg2 import OperationalError
from sqlalchemy.orm import Session
from sqlalchemy import func,text,asc #select, join
from typing import Optional
from app.models.user_model import User
from app.schemas import user_schema
from sqlalchemy.exc import IntegrityError
from app.schemas.user_avatar_schema import UserAvatar
from app.utils.others import alternate_true_false
from app.utils.others import gen
from app.utils.sql_utils import SQL_QUERY_DELAY_SECONDS, SQL_QUERY_MAX_RETRY, retry_on_operational_error

def get_users(db: Session, skip: int = 0, limit: int = 100)->list[User]:
    return db.query(User).offset(skip).limit(limit).all()
#
def get_users_by_id_greater_than(db: Session, id: int, skip: int = 0, limit: int = 100)-> list[User]:
    query = db.query(User).filter(User.id >= id)
    query = query.order_by(asc(User.id))
    query = query.limit(limit)
    users = query.all()
    return users

@retry_on_operational_error(SQL_QUERY_MAX_RETRY,SQL_QUERY_DELAY_SECONDS)
def get_user_by_username(db: Session, username: str) -> User:
    """ is_should_raise = next(gen)
    print(f'is should raise: {is_should_raise}')
    if(is_should_raise):
        raise OperationalError """
    return db.query(User).filter(User.username == username).first()

def flag_user(db: Session, username: str) -> Optional[User]:
    try:
        # Find the user by username
        user = db.query(User).filter(User.username == username).first()
        if user:
            # Set the is_outlaw field to True
            user.is_outlaw = True
            db.commit()  # Commit the changes to the database
            return user  # Return the updated user object
        else:
            return None  # User not found
    except Exception as e:
        db.rollback()  # Rollback the transaction in case of any error
        print(f"Error flagging user as outlaw: {e}")
        return None

def get_user_by_id(db: Session, id: str):
    return db.query(User).filter(User.id == id).first()

@retry_on_operational_error(SQL_QUERY_MAX_RETRY,SQL_QUERY_DELAY_SECONDS)
def create_user(db: Session, user: user_schema.User) -> Optional[user_schema.User]:
    try:
        db_user = User(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e: #duplicate username 
        db.rollback()
        print(f"Integrity error(user {user.username} already exist)")
        return None

def create_users_from_lst(db:Session, user_lst : list[str])->int:
    num_users_added = 0
    for user_str in user_lst:
        user_data = user_schema.UserCreate(username=user_str, is_outlaw=False, created_at=datetime.datetime.now(), updated_at=datetime.datetime(1970, 1, 1))  
        created_user = create_user(db, user_data)
        if created_user:
            num_users_added += 1
        # No need to catch IntegrityError here as it's handled within create_user
        # OperationalError retries are handled by the decorator
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
    
def get_top_100_users_without_avatar(db: Session)->list[dict]:
    try:
        # Write the raw SQL query
        sql_query = text("""
            SELECT id,username 
            FROM users_metadata 
            WHERE avatar = '' 
            LIMIT 20
        """)
        result = db.execute(sql_query).fetchall()
        usernames = [{'id': row[0], 'username': row[1]} for row in result]
        
        return usernames
    except Exception as e:
        print(f"Error: {e}")
        return []

def update_users_in_batch(db: Session, updates: list[UserAvatar]):
    try:
        update_query = "UPDATE users_metadata SET avatar = CASE id "
        guid_query = "guid = CASE id "

        ids = []
        for update_data in updates:
            user_id = update_data.id
            new_avatar = update_data.avatar
            new_guid = update_data.guid

            update_query += f"WHEN {user_id} THEN '{new_avatar}' "
            guid_query += f"WHEN {user_id} THEN {new_guid} "
            ids.append(str(user_id))

        update_query += "END, " + guid_query + "END "
        update_query += f"WHERE id IN ({', '.join(ids)})"
        db.execute(text(update_query))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False