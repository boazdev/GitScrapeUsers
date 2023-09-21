import requests

def get_users_by_url(url,headers) -> dict:
    response = requests.get(url=url,headers=headers)
    if response.status_code!=200:
        raise
    return response.json()

