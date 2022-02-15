from kafka import KafkaConsumer
from datetime import datetime
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


class LocationConsumer:
    @staticmethod
    def kafkaConsumer():
        # logger.info("kafkaConsumer")
        consumer = KafkaConsumer(
            TOPIC_LOCATION,
            bootstrap_servers=[KAFKA_SERVER],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        for location in consumer: 
            try:
                push_app_context()
                l = LocationService.create(location.value)
                logger.info(' %s, A new location with id %d and person id %d is created on location_ms!',datetime.now(),l.id,l.person_id)
            except Exception as e:
                logger.error("An exception occurred on kafkaConsumer %s",'division', exc_info=e)
            # Process(target=LocationService.create,args=(location.value,)).start()

    @staticmethod        
    def kafkaConsumerWithRetryConnection():
        while True:
            try:
                LocationConsumer.kafkaConsumer()
            except:
                logger.warning("Waiting kafka server")
                time.sleep(1)
                continue
            break