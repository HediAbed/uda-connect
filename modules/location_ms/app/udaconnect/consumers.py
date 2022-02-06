from kafka import KafkaConsumer
import os
import json
import logging
import sys
import time
from app import push_app_context
from app.udaconnect.services import LocationService
from multiprocessing import Process

TOPIC_LOCATION = os.environ["TOPIC_LOCATION"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]

logger = logging.getLogger()
logger.setLevel(logging.INFO)
# ch = logging.StreamHandler(sys.stdout)
# ch.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)
# logger.addHandler(ch)


class LocationConsumer:
    @staticmethod
    def kafkaConsumer():
        # logger.info("kafkaConsumer")
        push_app_context()
        consumer = KafkaConsumer(
            TOPIC_LOCATION,
            bootstrap_servers=[KAFKA_SERVER],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        for location in consumer: 
            try:
                LocationService.create(location.value)
            except:
                logger.warning("An exception occurred on kafkaConsumer")
            # Process(target=LocationService.create,args=(location.value,)).start()