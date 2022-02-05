
from multiprocessing import Process
from app.udaconnect.grpc.servers import PersonServer

def start_process():
    start_grpc_process()

def start_grpc_process():
    Process(target=PersonServer.server).start()