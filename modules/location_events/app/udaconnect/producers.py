from kafka import KafkaProducer
import os
from json import dumps
TOPIC_LOCATION = os.environ["TOPIC_LOCATION"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]
    
class LocationProducer:
    @staticmethod
    def kafkaProducer(locationMessage):
        producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,api_version=(0,11,5),value_serializer=lambda x: dumps(x).encode('utf-8'))
        producer.send(TOPIC_LOCATION,locationMessage)
        producer.flush()