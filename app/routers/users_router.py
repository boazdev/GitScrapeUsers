from fastapi import APIRouter, Depends,HTTPException, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.utils.github_utils import create_github_headers,create_github_url, users_from_json
from app.service.github_service import get_users_by_url
router = APIRouter(prefix="/users", tags=["users"])
from app.schemas.options_schema import OptionsIn
import anyio
import time
@router.get("/", response_model=dict, status_code=200)
def get_github_users():
    return {"users":[1,2,3,4,5]}

@router.post("/", response_model=dict, status_code=200)
def save_github_users(options: OptionsIn):
    headers=create_github_headers()
    url = create_github_url("a",5,1)
    print(f"options recieved: {options}")
    print(f"github url created: {url}")
    users_json = get_users_by_url(url,headers)
    users_lst = users_from_json(users_json)
    print(users_lst)
    return {"users_added":100,"users_current":300}

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