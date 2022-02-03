
from multiprocessing import Process
from app.udaconnect.consumers import LocationConsumer
from app.udaconnect.grpc.servers import ConnectionServer

def start_process():
    start_consumers_process()
    start_grpc_process()


def start_consumers_process():
    Process(target=LocationConsumer.kafkaConsumer).start()

def start_grpc_process():
    Process(target=ConnectionServer.server).start()
