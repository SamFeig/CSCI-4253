import grpc
from concurrent import futures
import time
from PIL import Image
import io

# import the generated classes
import lab6_pb2
import lab6_pb2_grpc

class addServicer(lab6_pb2_grpc.addServicer):
    def add(self, request, context):
        response = lab6_pb2.addMsg()
        response.a = request.a + request.b
        return response

class imageServicer(lab6_pb2_grpc.imageServicer):
    def image(self, request, context):
        response = lab6_pb2.addMsg()
        ioBuffer = io.BytesIO(request.img)
        i = Image.open(ioBuffer)
        response.a = i.size[0]
        response.b = i.size[1] 
        return response

# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

lab6_pb2_grpc.add_addServicer_to_server(addServicer(), server)

lab6_pb2_grpc.add_imageServicer_to_server(imageServicer(), server)

print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()
server.wait_for_termination()
