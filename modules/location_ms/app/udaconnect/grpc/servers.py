import time
import grpc
import logging
from concurrent import futures
from app.udaconnect.grpc.connection import connection_pb2_grpc
from app.udaconnect.grpc.servicers import ConnectionServicer

logger = logging.getLogger()
logger.setLevel(logging.INFO)
# TODO add it into processs.py and remove the other package grpcserver*
class ConnectionServer:
    @staticmethod
    def server():
        # Initialize gRPC server
        logger.info("# Initialize gRPC server")
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
        connection_pb2_grpc.add_ConnectionServiceServicer_to_server(ConnectionServicer(), server)
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