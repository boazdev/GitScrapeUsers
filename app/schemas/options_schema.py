from pydantic import BaseModel

class OptionsIn(BaseModel):
    min_repos: str = 1 
    """
    The minimum number of repositories a user must have to be added to the database.
    Default is 5.
    """
    delay: int = 0 #delay between requests to github
    max_users: int = 10000  #maxium number of users to scan

class OptionsHebrew(BaseModel):
    start_name: str = None #start the scraping from where we left off
    delay:  int = 0
    max_users: int = 10000

class KafkaRequest(BaseModel):
    batch_size: int = 1000
    wakeup_time_minutes: int = 60
    start_user_id: int = 0



