from fastapi import APIRouter, Depends,HTTPException, Response
from app.schemas.options_schema import OptionsIn,OptionsHebrew
from app.schemas.user_schema import UserCreate
from sqlalchemy.orm import Session
from app.database.db import get_db

from app.utils.github_utils import *
from app.service import github_service, file_service, users_service
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

@router.post("/start-hebrew",response_model=dict, status_code=200)
def start_scrape_hebrew_users(options: OptionsHebrew, db: Session = Depends(get_db)):
    hebrew_name_lst = file_service.extract_names_from_file("app\data\heb2eng.csv")
    print(f"number of hebrew names found in csv file: {len(hebrew_name_lst)}") #there should be at least 6346 rows in the file
    headers=create_github_headers()
    num_users_added=0
    for name in hebrew_name_lst:
        i=0
        num_pages=1
        while(i<num_pages):
            url = create_github_url(name,min_repos=0,page=i+1)
            users_json = github_service.try_get_users_by_url(url,headers,delay_seconds=10.0,max_retry=6)
            num_pages = users_json["payload"]["page_count"]
            username_lst = users_from_json(users_json)
            num_users_added+=users_service.create_users_from_lst(db,username_lst)
            print(f"num users added after page {i}: {num_users_added}")
            print(f"url: {url}, hebrew name:{name}")
            if(num_users_added>options.max_users):
                return {"users_added":num_users_added}
            time.sleep(float(options.delay))
            i+=1
    return {"users_added":num_users_added}

@router.post("/sort_heb_file", response_model=dict, status_code=200)
def sort_heb_file():
    hebrew_name_lst = file_service.extract_names_from_file("app\data\heb2eng.csv")
    sorted_list = sorted(list(set(name.lower() for name in hebrew_name_lst)))#sorted([name.lower() for name in hebrew_name_lst])

    data = {"hebrew_names": sorted_list}
    file_path = "sorted_names.json"
    file_service.write_json_data("app\data\heb_names.json",data)
    return {"sorted":"true"}

@router.post("/stop", response_model=dict, status_code=200)
def stop_scrape_github_users():
    return {"stopped":"true"}