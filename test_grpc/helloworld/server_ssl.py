
from concurrent import futures
import logging

import grpc
import helloworld_pb2
import helloworld_pb2_grpc


class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)


def serve():
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    with open('ssl/privkey.pem', 'rb') as f:
        private_key = f.read()
    with open('ssl/cert.pem', 'rb') as f:
        certificate_chain = f.read()
    server_credentials = grpc.ssl_server_credentials( ( (private_key, certificate_chain), ) )

    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    # Adding GreeterServicer to server omitted
    server.add_secure_port('localhost:50051', server_credentials)
    server.start()
    # Server sleep omitted
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()