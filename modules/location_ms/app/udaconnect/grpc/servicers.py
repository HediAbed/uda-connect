import time
import grpc
import logging
from concurrent import futures
from datetime import datetime
from app.udaconnect.grpc.connection import connection_pb2_grpc
from app.udaconnect.grpc.connection import connection_pb2 as connection__pb2
from app.udaconnect.services import LocationService
from app.udaconnect.schemas import LocationSchema
from app import push_app_context

DATE_FORMAT = "%Y-%m-%d"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ConnectionServicer(connection_pb2_grpc.ConnectionServiceServicer):
    def Get(self, request, context):
        push_app_context()
        format = '%Y-%m-%d'
        locations = LocationService.find_locations(request.person_id, datetime.strptime(request.start_date,DATE_FORMAT), datetime.strptime(request.end_date,DATE_FORMAT), request.meters)

        locations_pb2: connection__pb2.LocationMessage = []
        for _location in locations:
            logger.info(_location)
            locations_pb2.append(
            connection__pb2.LocationMessage(
                id= _location["id"],
                person_id= _location["person_id"],
                longitude= _location["longitude"],
                latitude= _location["latitude"],
                start_date= _location["start_date"],
                end_date= _location["end_date"],
                meters= _location["meters"],
                )
            )
        #.strftime("%Y-%m-%dT%H:%M:%S)"),
        logger.info(locations_pb2)
        result = connection__pb2.LocationMessageList()
        result.locations.extend(locations_pb2)
        # _location = LocationService.retrieve(request.id)
        # location = connection__pb2.LocationMessage(
        #     id=_location.id,
        #     person_id=_location.person_id,
        #     longitude=_location.longitude,
        #     latitude=_location.latitude,
        #     creation_time=_location.creation_time.strftime("%Y-%m-%dT%H:%M:%S)")
        # )
        # person = connection__pb2.PersonMessage(
        #     id=2222,
        #     company_name= "Alpha Omega Upholstery",
        #     last_name="Fargo",
        #     first_name="Taco"
        # )
        # first_connection = connection__pb2.ConnectionMessage(
        #     location=location,
        #     person=person
        # )
        # second_connection = connection__pb2.ConnectionMessage(
        #     location=location,
        #     person=person
        # )


        # result = connection__pb2.ConnectionMessageList()
        # result.connections.extend([first_connection, second_connection])

        return result