from asyncio.log import logger
from xmlrpc.client import boolean
import grpc
import os
from app.udaconnect.grpc.person import person_pb2 as person__pb2
from app.udaconnect.grpc.person import person_pb2_grpc

RPC_PERSON_SERVER = os.environ["RPC_PERSON_SERVER"]
RPC_PERSON_PORT = os.environ["RPC_PERSON_PORT"]

channel = grpc.insecure_channel(RPC_PERSON_SERVER+":"+RPC_PERSON_PORT)
stub = person_pb2_grpc.PersonServiceStub(channel)

class PersonClient:
    def exists(_id: int) -> boolean:
        person_id_request = person__pb2.PersonIDRequest(id=_id,)
        person_exits_response = stub.Exists(person_id_request)
        isPersonExists: boolean = person_exits_response.exists
        logger.info("isPersonExists")
        logger.info(isPersonExists)
        return isPersonExists
