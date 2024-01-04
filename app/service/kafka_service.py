import time
from confluent_kafka import Producer, KafkaError, Consumer, serialization
from confluent_kafka.admin import NewTopic, AdminClient, NewPartitions
from app.settings.config import get_settings

import json
class KafkaService:
    def __init__(self):
        self.kafka_url = get_settings().kafka_url
        print("kafka_url: ", self.kafka_url)
        self.producer_config = {
            "bootstrap.servers": self.kafka_url,#"kafka:9092",  # Replace with your Kafka broker(s)
            "client.id": "kafka_users_producer",
            
            #"value.serializer": serialization.Serializer(),#ConfluentKafkaSerializer(value_type='json'),
            #"key.serializer": Ser(value_type='string'),
        }
        self.producer : Producer = Producer(**self.producer_config)
        self.admin_client : AdminClient = AdminClient(self.producer_config)
        
    def topic_exists(self, topic):
        # Check if a Kafka topic exists
        #metadata = self.producer.list_topics(timeout=5)
        metadata = self.admin_client.list_topics().topics
        return topic in metadata

    def create_topic(self, topic_name,num_partitions):
        try:
            new_topic = NewTopic(
                topic=topic_name,
                num_partitions=num_partitions,  # Replace with the desired number of partitions
                replication_factor=1  # Replace with the desired replication factor
            )
            topics_dict: dict = self.admin_client.create_topics([new_topic])
        except KafkaError as e:
            print(e)
    def produce_usernames(self, topic,user_lst:list[str]):
        # Insert usernames into Kafka topic
        while True:
            usernames = user_lst #users_service.get_usernames(start_user_id, batch_size)
            if not usernames:
                break

            for username in usernames:
                json_value = {"username": username}
                #json_value = json.dumps(username)
                self.producer.produce(topic, key=username, value=username)
                #self.producer.produce(topic, key=None, value=username)
                self.producer.flush()
            break
            start_user_id += batch_size
            time.sleep(wakeup_time * 60)  # Convert wakeup_time to seconds

    def modify_topic_partitions(self, topic_name, new_partitions):
        try:
            topic_metadata = self.admin_client.list_topics().topics[topic_name]
            current_partitions = len(topic_metadata.partitions)
            if current_partitions < new_partitions:
                new_parts = [NewPartitions(topic_name, int(new_partitions))]
                self.admin_client.create_partitions(new_parts, validate_only=False)
                print(f"number of partitions is lower than {new_partitions}, added required partitions")
            else:
                print(f"Current number of partitions ({current_partitions}) is greater than or equal to the new number of partitions ({new_partitions}).")
        except KafkaError as e:
            raise

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

