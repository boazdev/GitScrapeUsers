from pydantic import BaseModel
class BaseOptions(BaseModel):
    by_api:bool = True #scrape by api, otherwise by html
    cookies:str = ""
    
class OptionsIn(BaseOptions):
    min_repos: str = 1 
    """
    The minimum number of repositories a user must have to be added to the database.
    Default is 5.
    """
    delay_seconds: int = 0 #delay between requests to github
    max_users: int = 10000  #maxium number of users to scan
    prefix_str : str = ""
    max_string_size : int = 3
    

class OptionsHebrew(BaseOptions):
    start_name: str = None #start the scraping from where we left off
    delay_seconds:  int = 0 # seconds
    max_users: int = 10000
    

class KafkaRequest(BaseModel):
    batch_size: int = 1000
    wakeup_time_minutes: int = 1
    start_user_id: int = 0

class KafkaModifyNumPartitionsRequest(BaseModel):
    num_partitions:int = 3



