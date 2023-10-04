from fastapi import APIRouter, Depends,HTTPException, Response

router  = APIRouter(prefix="/kafka_users",tags="inserting users to kafka_users from postgresql")

@router.post("start",response_model=dict,status_code=200)
def start_insert_kafka_users():
    return {"status":"started"}