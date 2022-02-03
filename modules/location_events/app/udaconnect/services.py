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
        LocationProducer.kafkaProducer(location)
    