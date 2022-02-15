
from multiprocessing import Process
from app.udaconnect.consumers import LocationConsumer
from app.udaconnect.grpc.servers import LocationServer

def start_process():
    start_grpc_process()
    start_consumers_process()


def start_consumers_process():
    Process(target=LocationConsumer.kafkaConsumerWithRetryConnection).start()

def start_grpc_process():
    Process(target=LocationServer.server).start()
