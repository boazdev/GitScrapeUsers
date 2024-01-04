from fastapi import APIRouter, Depends,HTTPException, Response
from app.schemas.options_schema import KafkaModifyNumPartitionsRequest, KafkaRequest
from app.service import kafka_service
from app.service.kafka_service import KafkaService
from app.service.users_service import get_users_by_id_greater_than
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.user_model import User
import time
import traceback
""" router  = APIRouter(prefix="/kafka_users",tags=["kafka_users producer"]) """

""" @router.post("/produce-users",response_model=dict,status_code=200) #TODO: num partitions of topics should be in constants python file
def start_insert_kafka_users(request: KafkaRequest, db: Session = Depends(get_db)):
    try:
        kafka_service = KafkaService()
        if not kafka_service.topic_exists("kafka_users"):
            print("kafka topic kafka_users does not exist, creating topic")
            kafka_service.create_topic("kafka_users",1)
        if not kafka_service.topic_exists("kafka_repositories"):
            print("kafka topic kafka_repositories does not exist, creating topic")
            kafka_service.create_topic("kafka_repositories",3)
        max_id: int = request.start_user_id
        while(True):
            # Start inserting usernames into the Kafka topic
            
            user_lst : list[User] = get_users_by_id_greater_than(db,id=max_id,skip=0,limit=request.batch_size) #todo: handle too many users error from postgres
            if len(user_lst) == 0:
                print("no new users added to postgres")
            else:
                max_id = user_lst[len(user_lst)-1].id +1
                user_lst = list(map(lambda item:item.username,user_lst))
                #print(f"users: {user_lst[0:10:1]}")
                kafka_service.produce_usernames(
                    "kafka_users",
                    user_lst
                )
                print(f"produced {len(user_lst)} usernames to kafka_users max_id: {max_id-1}")
                if len(user_lst)!=0:
                    print(f"first user: {user_lst[0]}, last user: {user_lst[len(user_lst)-1]}")
            time.sleep(request.wakeup_time_minutes * 60)  # Convert wakeup_time to seconds
        return {"message": "Data insertion into Kafka topic started successfully."}

    except Exception as e:
        print(traceback.print_exc())
        raise HTTPException(status_code=500, detail=str(e)) """

""" @router.post("/modify-partitions",response_model=str,status_code=200)
def modify_num_partiotions(request: KafkaModifyNumPartitionsRequest):
    try:
        kafka_service = KafkaService()
        kafka_service.modify_topic_partitions("kafka_repositories",request.num_partitions)
        return "modified"
    except Exception as e:
        print(e)
        print(traceback.print_exc())
        raise HTTPException(status_code=500, detail=str(e)) """

""" @router.get("/consume-users",response_model=dict, status_code=200)
def consume_kafka_users():
    kafka_service = KafkaService()
    if not kafka_service.topic_exists("kafka_users"):
            print("kafka topic kafka_users does not exist, creating topic")
            kafka_service.create_topic("kafka_users",1)
    kafka_service.consume_usernames("kafka_users",1500)
    return {"message:":"consumed kafka users successfully"} """