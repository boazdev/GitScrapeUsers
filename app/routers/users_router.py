from fastapi import APIRouter, Depends,HTTPException, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.utils.github_utils import create_github_headers,create_github_url, users_from_json
from app.service.github_service import get_users_by_url
router = APIRouter(prefix="/users", tags=["users"])
from app.schemas.options_schema import OptionsIn
from app.service import users_service
from app.database.db import get_db
from app.schemas import user_schema
import anyio
import time

@router.get("/", response_model=dict, status_code=200)
def get_db_github_users(skip: int = 0, limit: int = 100,db:Session=Depends(get_db)):
    usernames_lst : list[user_schema.User] = users_service.get_users(db, skip,limit)
    usernames_lst_serial = list(map(lambda x:{"id":x.id, "username":x.username},usernames_lst))
    return {"users":usernames_lst_serial, "number_db_users":users_service.get_num_users(db)}

@router.get("/username/{username}",response_model=user_schema.User, status_code=200)
def get_user_by_username(username:str, db: Session = Depends(get_db)):
    return users_service.get_user_by_username(db,username)


""" @router.post("/",response_model= user_schema.User,status_code=201)
def create_user(username:user_schema.UserCreate, db: Session = Depends(get_db)):
    resp = users_service.create_user(db,username)
    if resp==None:
        raise HTTPException(400,"Username already exist")
    return resp
 """
""" @router.delete("/",response_model=str, status_code=200)
def delete_all_users(db:Session=Depends(get_db)):
    resp = users_service.delete_all(db)
    return resp """


