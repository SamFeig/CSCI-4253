import grpc
import struct
import sys
from time import perf_counter

# import the generated classes
import lab6_pb2
import lab6_pb2_grpc

if len(sys.argv) != 4:
    print("\npython grpc-client.py <server address> <endpoint> <iterations>")
    exit()

addr = sys.argv[1] + ':50051'

endpoint = sys.argv[2]
num_iterations = sys.argv[3]
n = int(num_iterations)

img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()

#Open gRPC channel
channel = grpc.insecure_channel(addr)

#Image service
if(endpoint == 'image'):
    stub = lab6_pb2_grpc.imageStub(channel)
    count = 1
    start = perf_counter()

    while(count <= n):
        number = lab6_pb2.imageMsg(img=img)
        response = stub.image(number)
        print(response.a, response.b)
        count += 1

    total_time = perf_counter() - start
    print(str(total_time/n * 1000) + ' ms')

#Add service
else:
    stub = lab6_pb2_grpc.addStub(channel)
    count = 1
    start = perf_counter()

    while(count <= n):
        number = lab6_pb2.addMsg(a=2, b=3)
        response = stub.add(number)
        print(response.a)
        count += 1

    total_time = perf_counter() - start
    print(str(total_time/n * 1000) + ' ms')