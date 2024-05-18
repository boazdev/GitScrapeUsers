import os
import re
import requests
import time
from typing import Dict, Optional
import asyncio #todo: fetch data with async httpx httpx.AsyncClient()
from lxml import html
import json

from app.utils.sql_utils import retry_on_fetch_error

def get_users_by_url(url:str,headers:dict, by_api:bool = True) -> Optional[dict]:
    response = requests.get(url=url,headers=headers)
    if response.status_code!=200:
        print(f'request failed. error code: {response.status_code}')
        return None
    if(by_api):
        return response.json()
    else:
        return extract_json_from_script(response.text)

def try_get_users_by_url(url:str,headers:dict,delay_seconds:float = 10.0,max_retry:int = 0,by_api:bool=True) -> Optional[dict] :
    while(max_retry>=0):
        response = get_users_by_url(url,headers,by_api=by_api)
        if response==None:
            max_retry-=1
        else:
            return response
        time.sleep(delay_seconds)
        
        print(f"waiting {delay_seconds} seconds")
    return None

def extract_json_from_script(html_string:str):
    """Extracts JSON content from the specified script element in the HTML string.

    Args:
        html_string: The HTML string containing the script element.

    Returns:
        The extracted JSON content as a Python dictionary, or None if not found.
    """

    tree = html.fromstring(html_string)
    script = tree.xpath("//script[@type='application/json' and @data-target='react-app.embeddedData']")

    if script:
        script_text = script[0].text_content().strip()
        try:
            return json.loads(script_text)
        except json.JSONDecodeError:
            print("Error: Invalid JSON content in the script element.")
            return None
    else:
        print("Script element not found.")
        return None

def get_shit2(shit:str):
    return "shit"

@retry_on_fetch_error(100,1)
def get_user_data_by_api(username:str) -> Optional[dict]:
    response = requests.get(f'https://api.github.com/users/{username}')
    if response.status_code!=200:
        print(f'request failed. error code: {response.status_code}')
        return None
    else:
        return response.json()

def get_shit(shit:str):
    return "shit"

@retry_on_fetch_error(10, 1)
def get_user_data_by_html(username: str) -> Optional[dict]:
    response = requests.get(f'https://github.com/{username}')
    if response.status_code != 200:
        print(f'Request failed. Error code: {response.status_code}')
        return None
    else:
        html_content = response.text
        """ print(html_content[0:6000:1])
        data_dir = os.path.join(os.getcwd(), 'app/data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # Write the HTML content to a file
        file_path = os.path.join(data_dir, f'{username}.html')
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html_content) """

        avatar_pattern = r'<meta property="og:image" content="([^"]+)" />'
        avatar_match = re.search(avatar_pattern, html_content)
        if avatar_match:
            avatar_url = avatar_match.group(1)
        else:
            avatar_url = None
        print(f'avatar url: {avatar_url}')

        guid_pattern = r'u/(\d+)'
        guid_match = re.search(guid_pattern, avatar_url) if avatar_url else None
        if guid_match:
            guid = guid_match.group(1)
        else:
            guid = None
        print(f'guid: {guid}')
        if avatar_url and guid:
            return {'guid': guid, 'avatar_url': avatar_url}
        else:
            return None