from fastapi import APIRouter, Depends,HTTPException, Response
from app.schemas.options_schema import OptionsIn
from sqlalchemy.orm import Session
from app.database.db import get_db

from app.utils.github_utils import *
from app.service import github_service
import time
router = APIRouter(prefix="/scrape", tags=["github users scraper"])

@router.post("/start", response_model=dict, status_code=200) #todo: use app.state 
def start_scrape_github_users(options: OptionsIn):
    headers=create_github_headers()
    url = create_github_url("a",min_repos=options.min_repos,page=1)
    users_scanned = 0
    curr_page=1
    while(users_scanned<options.max_users):
        users_json = github_service.try_get_users_by_url(url,headers,delay_seconds=10.0,max_retry=6)
        if(users_json==None):
            return {"error":f"error scraping users page: {curr_page}"}
        num_pages = users_json["payload"]["page_count"]
        print(f'users scanned: {users_from_json(users_json)} num scanned: {users_scanned+10}')
        users_scanned+=10
        curr_page+=1
        url = create_github_url("a",min_repos=options.min_repos,page=curr_page)
        time.sleep(float(options.delay))
    return {"started":"true"}

@router.post("/stop", response_model=dict, status_code=200)
def stop_scrape_github_users():
    return {"stopped":"true"}