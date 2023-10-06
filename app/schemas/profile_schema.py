from pydantic import BaseModel

class Profile(BaseModel): #LINKED IN PROFILES
    id: int
    name: str
    