import logging
from datetime import datetime
from app.udaconnect.schemas import LocationSchema
from app.udaconnect.services import LocationService
from flask import request , Response
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa

logger = logging.getLogger()
logger.setLevel(logging.INFO)

@api.route("/locations/events")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self):
        try:
            logger.info(' %s, A new location with person id %d is sent to the location_ms!',datetime.now(),request.get_json()["person_id"])
            LocationService.create(request.get_json())
        except:
            logger.error(' %s, An issue ocured, please make sure you are inserting the right fields',datetime.now())
            Response(status=400)
        return Response(status=202)