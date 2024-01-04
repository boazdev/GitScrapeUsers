import requests
import time
from typing import Optional
import asyncio #todo: fetch data with async httpx httpx.AsyncClient()
from lxml import html
import json

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


    