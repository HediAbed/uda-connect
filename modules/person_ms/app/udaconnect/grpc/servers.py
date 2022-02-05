import time
import grpc
import logging
from concurrent import futures
from app.udaconnect.grpc.person import person_pb2_grpc
from app.udaconnect.grpc.servicers import PersonServicer

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class PersonServer:
    @staticmethod
    def server():
        # Initialize gRPC server
        logger.info("# Initialize gRPC server")
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
        person_pb2_grpc.add_PersonServiceServicer_to_server(PersonServicer(), server)
        print("Server starting on port 5005...")
        server.add_insecure_port("[::]:5005")
        server.start()
        # Keep thread alive
        logger.info("# Keep grpc thread alive")
        try:
            while True:
                time.sleep(86400)
        except KeyboardInterrupt:
            server.stop(0)
