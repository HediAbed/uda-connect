import logging
from typing import Dict
from app.udaconnect.schemas import LocationSchema
from app.udaconnect.producers import LocationProducer

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")

class LocationService:
    @staticmethod
    def create(location: Dict):
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")
        if 'person_id' not in  location:
            logger.warning(f"person_id is a required field")
            raise Exception(f"person_id is a required field")
        if 'creation_time' not in  location:
            logger.warning(f"creation_time is a required field")
            raise Exception(f"creation_time is a required field")
        if 'latitude' not in  location:
            logger.warning(f"latitude is a required field")
            raise Exception(f"latitude is a required field")
        if 'longitude' not in  location:
            logger.warning(f"longitude is a required field")
            raise Exception(f"longitude is a required field")
        LocationProducer.kafkaProducer(location)
