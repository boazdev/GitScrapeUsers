from fastapi import APIRouter, Depends,HTTPException, Response
from fastapi.types import UnionType
from app.schemas.options_schema import BaseOptions, OptionsIn,OptionsHebrew
from app.schemas.user_schema import UserCreate
from app.schemas.profile_schema import Profile
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.utils.bruteforce_utils import *
from app.utils.github_utils import *
from app.service import git_ranker_service, github_service, file_service, users_service, profiles_service
import time
router = APIRouter(prefix="/scrape", tags=["github users scraper"])

@router.post("/start-bruteforce", response_model=dict, status_code=200) #todo: use app.state BRUTEFORCE
def start_scrape_github_users(options: OptionsIn, db: Session = Depends(get_db)):
    num_users_added = 0
    for str_lst in bruteforce_lst_generator(options.prefix_str,options.max_string_size):
        num_users_added += scrape_from_str_lst(str_lst=str_lst,is_fullname=False,db=db,options=options)["users_added"]
        if num_users_added >= options.max_users:
            return {"num_users_added":num_users_added}
    return {"num_users_added":num_users_added}

@router.post("/start-hebrew",response_model=dict, status_code=200)
def start_scrape_hebrew_users(options: OptionsHebrew, db: Session = Depends(get_db)):
    hebrew_name_data = file_service.read_json("app\data\heb_names.json")#file_service.extract_names_from_file("app\data\heb2eng.csv")
    hebrew_name_lst = hebrew_name_data["hebrew_names"]
    print(f"number of hebrew names found in heb_names.json file: {len(hebrew_name_lst)}") #there should be at least 6346 rows in the file
    return scrape_from_str_lst(str_lst=hebrew_name_lst,is_fullname=False,db=db,options=options)


@router.post("/start-linkedin",response_model=dict, status_code=200)
def start_scrape_linkedin_users(options: OptionsHebrew, db: Session = Depends(get_db)):
    profiles_list:list[Profile] = profiles_service.get_linkedin_profiles(db)
    #profiles_list = list(map(lambda profile: profile.name, profiles_list)) #todo:remove special characters from name, handle cases where fullname contains three strings
    users_added = scrape_linkedin_from_profiles_lst(profiles_lst=profiles_list,is_fullname=True,db=db,options=options)
    return users_added

""" @router.post("/sort_heb_file", response_model=dict, status_code=200)
def sort_heb_file():
    hebrew_name_lst = file_service.extract_names_from_file("app\data\heb2eng.csv")
    sorted_list = sorted(list(set(name.lower() for name in hebrew_name_lst)))#sorted([name.lower() for name in hebrew_name_lst])

    data = {"hebrew_names": sorted_list}
    file_path = "sorted_names.json"
    file_service.write_json_data("app\data\heb_names.json",data)
    return {"sorted":"true"} """


def scrape_from_str_lst(str_lst:list[str], is_fullname:bool, db:Session,options: BaseOptions)->dict:
    headers=create_github_headers(by_api=options.by_api,cookies=options.cookies)
    num_users_added=0
    for name in str_lst:
        i=0
        num_pages=1
        while(i<num_pages):
            if is_fullname:
                print(name.split(' '))
                [firstname,lastname] = name.split(' ')[0:2:1]
                url = create_github_fullname_url(firstname,lastname,min_repos=0,page=i+1)
            else:
                url = create_github_url(name,min_repos=0,page=i+1)
            users_json = github_service.try_get_users_by_url(url,headers,delay_seconds=10.0,max_retry=6,by_api=options.by_api) 
            num_pages = users_json["payload"]["page_count"] # returns 0 if no user found
            username_lst = users_from_json(users_json) # returns empty list if no user found
            num_users_added+=users_service.create_users_from_lst(db,username_lst)
            print(f"num users added after page {i+1}: {num_users_added}")
            print(f"url: {url}, hebrew name:{name}, users:{username_lst}")
            if(num_users_added>options.max_users):
                return {"users_added":num_users_added}
            time.sleep(float(options.delay_seconds))
            i+=1
    return {"users_added":num_users_added}

def scrape_linkedin_from_profiles_lst(profiles_lst:list[Profile], is_fullname:bool, db:Session,options: BaseOptions)->dict:
    headers=create_github_headers(by_api=options.by_api,cookies=options.cookies)
    num_users_added=0
    for profile in profiles_lst:
        i=0
        num_pages=1
        while(i<num_pages):
            if is_fullname:
                print(profile.name.split(' '))
                [firstname,lastname] = profile.name.split(' ')[0:2:1]
                url = create_github_fullname_url(firstname,lastname,min_repos=0,page=i+1)
            else:
                url = create_github_url(profile.name,min_repos=0,page=i+1)
            users_json = github_service.try_get_users_by_url(url,headers,delay_seconds=10.0,max_retry=6,by_api=options.by_api) 
            num_pages = users_json["payload"]["page_count"] # returns 0 if no user found
            username_lst = users_from_json(users_json) # returns empty list if no user found
            for username in username_lst:
                git_ranker_service.update_user_linkedin_id(username,profile.id)
            num_users_added+=users_service.create_users_from_lst(db,username_lst)
            print(f"num users added after page {i+1}: {num_users_added}")
            print(f"url: {url}, hebrew name:{profile.name}, users:{username_lst}")
            if(num_users_added>options.max_users):
                return {"users_added":num_users_added}
            time.sleep(float(options.delay_seconds))
            i+=1
    return {"users_added":num_users_added}

def create_bruteforce_list():
    pass