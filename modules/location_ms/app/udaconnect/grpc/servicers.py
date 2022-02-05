from typing import List
import logging
from datetime import datetime
from app.udaconnect.grpc.location import location_pb2_grpc
from app.udaconnect.grpc.location import location_pb2 as location__pb2
from app.udaconnect.services import LocationService

from app import push_app_context

from app.udaconnect.models import Location

DATE_FORMAT = "%Y-%m-%d"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Get(self, request, context):
        push_app_context()
        locations: List[Location] = LocationService.find_locations(request.person_id, datetime.strptime(request.start_date,DATE_FORMAT), datetime.strptime(request.end_date,DATE_FORMAT), request.meters)
        # logger.info(locations)
        result = location__pb2.LocationMessageListResponse()
        # result.locations.extend(locations_pb2)
        for _location in locations:
            # logger.info(_location)
            locationMessage = location__pb2.LocationMessage(
                id= _location.id,
                person_id= _location.person_id,
                longitude= _location.longitude,
                latitude= _location.latitude,
                creation_time= _location.creation_time.strftime("%Y-%m-%dT%H:%M:%S"),
                )
            result.locations.extend([locationMessage])
        return result