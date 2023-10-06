from sqlalchemy.orm import Session #LINKED IN PROFILES SERVICE. FETCH USERS AND INSERTS TO GIT USERS
from sqlalchemy import func,text #select, join
from app.models.profile_model import Profile
import json
#SELECT profiles.url, profiles.name from profiles

def get_linkedin_profiles(db: Session)->list[Profile]:
    return db.query(Profile).all()

def get_2(db:Session)->dict:
    custom_query = text("SELECT * FROM users;")

    # Execute the query and fetch the results
    results = db.execute(custom_query)

    # Convert the results to a list of dictionaries
    result_data = [dict(row) for row in results]

    # Convert the list to JSON
    json_result = json.dumps(result_data)
    return json_result
    # Close the session
    