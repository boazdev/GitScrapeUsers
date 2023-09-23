import requests
import time
from typing import Optional
def get_users_by_url(url:str,headers:dict) -> Optional[dict]:
    response = requests.get(url=url,headers=headers)
    if response.status_code!=200:
        print(f'request failed. error code: {response.status_code}')
        return None
    return response.json()

def try_get_users_by_url(url:str,headers:dict,delay_seconds:float = 10.0,max_retry:int = 0) -> Optional[dict] :
    while(max_retry>=0):
        response = get_users_by_url(url,headers)
        if response==None:
            max_retry-=1
        else:
            return response
        time.sleep(delay_seconds)
        
        print(f"waiting {delay_seconds} seconds")
    return None
    