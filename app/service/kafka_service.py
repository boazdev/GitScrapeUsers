import time
from confluent_kafka import Producer, KafkaError, Consumer
from confluent_kafka.admin import NewTopic, AdminClient

class KafkaService:
    def __init__(self):
        # Initialize Kafka producer configuration
        self.producer_config = {
            "bootstrap.servers": "kafka:9092",  # Replace with your Kafka broker(s)
            "client.id": "kafka_users_producer"
        }
        self.producer : Producer = Producer(**self.producer_config)
        self.admin_client : AdminClient = AdminClient(self.producer_config)
        
    def topic_exists(self, topic):
        # Check if a Kafka topic exists
        metadata = self.producer.list_topics(timeout=5)
        metadata = self.admin_client.list_topics(topic)
        print(f"metadata: {metadata} type: {type(metadata)}")
        return True

    def create_topic(self, topic):
        # Create a Kafka topic if it doesn't exist
        try:
            if not self.topic_exists(topic):
                self.admin_client.create_topics([topic])
        except KafkaError as e:
            print(e)
    def produce_usernames(self, topic, batch_size, wakeup_time, start_user_id):
        # Insert usernames into Kafka topic
        while True:
            usernames = ["1","2","3"] #users_service.get_usernames(start_user_id, batch_size)
            if not usernames:
                break

            for username in usernames:
                self.producer.produce(topic, key=None, value=username)
                self.producer.flush()
            break
            start_user_id += batch_size
            time.sleep(wakeup_time * 60)  # Convert wakeup_time to seconds