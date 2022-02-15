import logging, sys
from datetime import datetime, timedelta
from typing import Any, Dict, List
from google.protobuf.json_format import MessageToJson
from app.udaconnect.schemas import ConnectionSchema
from app.udaconnect.grpc.clients import LocationClient, PersonClient

# logging.basicConfig(level=logging.WARNING)
# logger = logging.getLogger("udaconnect-api")

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class ConnectionService:
    @staticmethod
    def find_contacts(person_id: int, start_date: datetime, end_date: datetime, meters=5):
        """
        Finds all Person who have been within a given distance of a given Person within a date range.

        This will run rather quickly locally, but this is an expensive method and will take a bit of time to run on
        large datasets. This is by design: what are some ways or techniques to help make this data integrate more
        smoothly for a better user experience for API consumers?
        """

        locations= LocationClient.get(person_id, start_date, end_date, meters).locations
        persons_ids = list(set([location.person_id for location in locations]))
        
        persons = PersonClient.get(persons_ids).persons
        person_map: Dict[int, Any] = {person.id: person for person in persons}


        result= []
        for location in locations:
            try:
                person = person_map[location.person_id]
            except:
                logger.error("location %d with none existing person id %d",location.id,location.person_id)
                continue
            result.append(
                {
                    "person": {
                        "id":person.id,
                        "first_name":person.first_name,
                        "last_name":person.last_name,
                        "company_name":person.company_name
                        },
                    "location":{
                        "id":location.id,
                        "person_id":location.person_id,
                        "longitude":location.longitude,
                        "latitude":location.latitude,
                        "creation_time":location.creation_time
                    }
                }
            )
        return result