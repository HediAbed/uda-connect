from datetime import datetime
import logging
from app.udaconnect.models import  Location
from app.udaconnect.schemas import (
    LocationSchema,
)
from app.udaconnect.services import LocationService
from app.udaconnect.consumers import LocationConsumer
from flask import request, Response
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa


# TODO: This needs better exception handling
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# @api.route("/locations")
@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        try:
            location: Location = LocationService.retrieve(location_id)
        except:
            logger.error("location not found")
            return Response('{"error":"Location not found"}', 404, mimetype='application/json')
        return location