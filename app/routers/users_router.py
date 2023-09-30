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
    for user in usernames_lst:
        print(f"username: {user.username} type:{type(usernames_lst)}")
    usernames_lst_serial = list(map(lambda x:{x.id, x.username},usernames_lst))
    return {"users":usernames_lst_serial, "number_db_users":users_service.get_num_users(db)}

@router.post("/", response_model=dict, status_code=200)
def start_scrape_github_users(options: OptionsIn):
    headers=create_github_headers()
    url = create_github_url("a",5,1)
    print(f"options recieved: {options}")
    print(f"github url created: {url}")
    users_json = get_users_by_url(url,headers)
    users_lst = users_from_json(users_json)
    print(users_lst)
    return {"users_added":100,"users_current":300}

@router.get("/username/{username}",response_model=user_schema.User, status_code=200)
def get_user_by_username(username:str, db: Session = Depends(get_db)):
    return users_service.get_user_by_username(db,username)


@router.post("/{user}",response_model= user_schema.User,status_code=201)
def create_user(username:user_schema.UserCreate, db: Session = Depends(get_db)):
    resp = users_service.create_user(db,username)
    if resp==None:
        raise HTTPException(400,"Username already exist")
    return resp

@router.delete("/",response_model=str, status_code=200)
def delete_all_users(db:Session=Depends(get_db)):
    resp = users_service.delete_all(db)
    return resp



async def fake_video_streamer():
    for i in range(1, 11):
        await anyio.sleep(2)
        yield f"Data point {i}\n"
        #await asyncio.sleep(1)  # Simulate some asynchronous work

def fake_data_streamer():
    for i in range(10):
        yield b'some fake data\n\n'
        time.sleep(1.0)
        

@router.get("/stream-data")
async def stream_data():
    return StreamingResponse(fake_video_streamer(), media_type='text/event-stream')


""" 
@router.post("/createUser", response_model=UserSchema.BaseUser)
def create_user(user: UserSchema.BaseUser, db: Session = Depends(getDataBase)):

    newUser = UserService.createUser(db=db, user=user)

    return newUser """ 