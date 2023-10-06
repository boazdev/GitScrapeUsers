from fastapi import APIRouter, Depends,HTTPException, Response
from schemas.options_schema import KafkaRequest
from service.kafka_service import KafkaService
router  = APIRouter(prefix="/kafka_users",tags="inserting users to kafka_users from postgresql")

@router.post("kafka-users",response_model=dict,status_code=200)
def start_insert_kafka_users(request: KafkaRequest):
    try:
        # Initialize Kafka and PostgreSQL services
        kafka_service = KafkaService()
        #users_service = UsersService()

        # Check if the Kafka topic "kafka_users" exists, create it if not
        if not kafka_service.topic_exists("kafka_users"):
            kafka_service.create_topic("kafka_users")

        # Start inserting usernames into the Kafka topic
        kafka_service.produce_usernames(
            "kafka_users",
            request.batch_size,
            request.wakeup_time_minutes,
            request.start_user_id
            
        )

        return {"message": "Data insertion into Kafka topic started successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))