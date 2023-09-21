from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/github-users", response_model=dict, status_code=200)
def get_github_users():
    return {"users":[1,2,3,4,5]}

@router.post("/test", response_model=dict, status_code=200)
def save_github_users():
    return {"users_added":100,"users_current":300}

""" 
@router.post("/createUser", response_model=UserSchema.BaseUser)
def create_user(user: UserSchema.BaseUser, db: Session = Depends(getDataBase)):

    newUser = UserService.createUser(db=db, user=user)

    return newUser """ 