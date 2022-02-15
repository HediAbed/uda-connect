from datetime import datetime
from app.udaconnect.schemas import ConnectionSchema

from app.udaconnect.services import ConnectionService
from flask import request
from flask_accepts import responds
from flask_restx import Namespace, Resource
from typing import Optional

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa


@api.route("/connections")
class ConnectionDataResource(Resource):
    @responds(schema=ConnectionSchema, many=True)
    def get(self):
        start_date: datetime = datetime.strptime(request.args["start_date"], DATE_FORMAT)
        end_date: datetime = datetime.strptime(request.args["end_date"], DATE_FORMAT)
        distance: Optional[int] = request.args.get("distance", 5)
        person_id: Optional[int] = request.args["person_id"]

        results = ConnectionService.find_contacts(
            person_id=int(person_id),
            start_date=start_date,
            end_date=end_date,
            meters=int(distance),
        )
        return results
