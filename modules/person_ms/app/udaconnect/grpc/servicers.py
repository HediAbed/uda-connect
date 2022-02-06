from typing import List
import logging
from datetime import datetime
from xmlrpc.client import boolean
from app.udaconnect.grpc.person import person_pb2_grpc
from app.udaconnect.grpc.person import person_pb2 as person__pb2
from app.udaconnect.services import PersonService
from app.udaconnect.models import Person

from app import push_app_context

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class PersonServicer(person_pb2_grpc.PersonServiceServicer):
    def Get(self, request, context):
        push_app_context()
        logger.info("ids: request => ")
        logger.info(request.ids)
        persons: List[Person] = PersonService.retrieve_all_by_ids(request.ids)
        logger.info("Persons: response => ")
        logger.info(persons)
        result = person__pb2.PersonMessageListResponse()
        for _perosn in persons:
            personMessage = person__pb2.PersonMessage(
                id=_perosn.id,
                first_name=_perosn.first_name,
                last_name=_perosn.last_name,
                company_name=_perosn.company_name,
            )
            result.persons.extend([personMessage])
        return result

    def Exists(self, request, context):
        push_app_context()
        isPersonExists: boolean = PersonService.exists(request.id)
        logger.info(isPersonExists)
        result = person__pb2.PersonExistsResponse(
            exists=isPersonExists,
        )
        return result