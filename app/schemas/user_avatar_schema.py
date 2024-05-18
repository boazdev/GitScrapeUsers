from pydantic import BaseModel

class UserAvatar(BaseModel): #LINKED IN PROFILES
    id: int
    guid: int
    avatar: str
    username: str