import json
from typing import Optional
import requests

from app.settings.config import get_settings

def update_user_linkedin_id(username:str, profile_id:int) -> Optional[dict]:
    settings = get_settings()
    url: str = settings.ranker_api_url
    api_key: str = settings.ranker_api_key
    body:dict = {"apiKey":api_key,"profileId":profile_id}
    body = json.dumps(body)
    headers = {'Content-Type': 'application/json'}
    print(f'sending patch request to git ranker api with username: {username}, profile_id:{profile_id}')
    response = requests.patch(url=url,data=body, headers=headers)
    if response.status_code not in [200,201]:
        print(f'sending patch request to git ranker api failed. error code: {response.status_code}')
        return None
    else:
        return response.json()