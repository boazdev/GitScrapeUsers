from pydantic import BaseModel

class OptionsIn(BaseModel):
    min_repos : str = 5 
    """
    The minimum number of repositories a user must have to be added to the database.
    Default is 5.
    """
    delay : int = 0
    max_users : int = 10000


