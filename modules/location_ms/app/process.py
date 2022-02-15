
from multiprocessing import Process
from app.udaconnect.consumers import LocationConsumer
from app.udaconnect.grpc.servers import LocationServer

def start_process():
    start_consumers_process()
    start_grpc_process()


def start_consumers_process():
    try:
        Process(target=LocationConsumer.kafkaConsumer).start()
    except:
        Process(target=LocationConsumer.kafkaConsumer).start()

def start_grpc_process():
    Process(target=LocationServer.server).start()
