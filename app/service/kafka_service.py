import time
from confluent_kafka import Producer, KafkaError, Consumer
from confluent_kafka.admin import NewTopic, AdminClient
from app.settings.config import get_settings
class KafkaService:
    def __init__(self):
        # Initialize Kafka producer configuration
        settings = get_settings()
        print(f"settings: {settings}")
        self.kafka_url = get_settings().kafka_url
        print("kafka_url: ", self.kafka_url)
        self.producer_config = {
            "bootstrap.servers": self.kafka_url,#"kafka:9092",  # Replace with your Kafka broker(s)
            "client.id": "kafka_users_producer"
        }
        self.producer : Producer = Producer(**self.producer_config)
        self.admin_client : AdminClient = AdminClient(self.producer_config)
        
    def topic_exists(self, topic):
        # Check if a Kafka topic exists
        #metadata = self.producer.list_topics(timeout=5)
        metadata = self.admin_client.list_topics().topics
        return topic in metadata

    def create_topic(self, topic_name):
        try:
            new_topic = NewTopic(
                topic=topic_name,
                num_partitions=1,  # Replace with the desired number of partitions
                replication_factor=1  # Replace with the desired replication factor
            )
            self.admin_client.create_topics([new_topic])
        except KafkaError as e:
            print(e)
    def produce_usernames(self, topic,user_lst:list[str]):
        # Insert usernames into Kafka topic
        while True:
            usernames = user_lst #users_service.get_usernames(start_user_id, batch_size)
            if not usernames:
                break

            for username in usernames:
                self.producer.produce(topic, key=None, value=username)
                self.producer.flush()
            break
            start_user_id += batch_size
            time.sleep(wakeup_time * 60)  # Convert wakeup_time to seconds

    def consume_usernames(self, topic, max_users):
        consumer = Consumer({
        'bootstrap.servers': 'kafka:9092',
        'auto.offset.reset': 'latest',  # Start from the latest message
        "client.id": "kafka_users_consumer",
        "group.id":"kafka_users_consumers"
        })
        num_users = 0
        consumer.subscribe([topic])
        while(num_users<max_users):
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f'Error while consuming: {msg.error()}')
            else:   
                # Parse the received message
                value = msg.value().decode('utf-8')
                num_users+=1
                if num_users%2==0:
                    print(f'Consumed {num_users} users, Received current username: {value}')
        consumer.close()

