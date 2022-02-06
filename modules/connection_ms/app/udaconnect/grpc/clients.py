from typing import List
from xmlrpc.client import boolean
import logging
import grpc
import os , sys
from datetime import datetime
from app.udaconnect.grpc.person import person_pb2 as person__pb2
from app.udaconnect.grpc.person import person_pb2_grpc
from app.udaconnect.grpc.location import location_pb2 as location__pb2
from app.udaconnect.grpc.location import location_pb2_grpc

DATE_FORMAT = "%Y-%m-%d"

RPC_PERSON_SERVER = os.environ["RPC_PERSON_SERVER"]
RPC_PERSON_PORT = os.environ["RPC_PERSON_PORT"]

RPC_LOCATION_SERVER = os.environ["RPC_LOCATION_SERVER"]
RPC_LOCATION_PORT = os.environ["RPC_LOCATION_PORT"]

person_channel = grpc.insecure_channel(RPC_PERSON_SERVER+":"+RPC_PERSON_PORT)
person_stub = person_pb2_grpc.PersonServiceStub(person_channel)

location_channel = grpc.insecure_channel(RPC_LOCATION_SERVER+":"+RPC_LOCATION_PORT)
location_stub = location_pb2_grpc.LocationServiceStub(location_channel)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class PersonClient:
    def get(_ids: List[int]):
        person_id_request = person__pb2.PersonIDsRequest(ids=_ids)
        persons_response = person_stub.Get(person_id_request)
        return persons_response

class LocationClient:
    def get(person_id: int, start_date: datetime, end_date: datetime, meters:int =5):
        location_request = location__pb2.LocationRequest(
            person_id=person_id,
            start_date=start_date.strftime(DATE_FORMAT),
            end_date=end_date.strftime(DATE_FORMAT),
            meters=meters,
        )
        location_response = location_stub.Get(location_request)
        return location_response