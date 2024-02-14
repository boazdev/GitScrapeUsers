from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str


    
class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    is_outlaw: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True