# gRPC Server Implementation

To build the gRPC server, you should follow [this tutorial for a sample python server and client](https://grpc.io/docs/tutorials/basic/python/).

You'll need to install the Protobuf tools
```
sudo apt install protobuf-compiler
sudo pip3 install grpcio-tools
```

#### What you need to do for the gRPC section

You need to build a gRPC service that implements an `add` and `image` message and has the same functionality as the REST implementation.

The reference implementation used these types:
```
message addMsg {
  int32 a = 1;
  int32 b = 2;
}

message imageMsg {
    bytes img=1;
}
```

The `bytes` type can be used to transport an array of bytes. The corresponding code to initialize the `imageMsg` type looks like:
```
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    data = lab6_pb2.imageMsg(img=img)
```

You should implement the `add` service first -- that will walk you through the basic steps of creating a `protobuf` specification and geneating the code. After that, you should add the `image` endpoint. You can transport the image using the `bytes` designation.

You may see warning in the protocol buffer tutorial that protocol buffers (and gRPC) really aren't designed to transport large messages, but it will work fine for this lab.

The remainder of the steps involved following the [python tutorial example](https://grpc.io/docs/tutorials/basic/python/) and adapting the types.

As with the REST exmaple, you should have a client to accept a command-line argument indicating the endpoint to be tested and the number of iterations to test. For example:
```
python grpc-client.py localhost add 1000
```
would run the `add` endpoint 1000 times against the server on the `localhost` and then report the time taken divided by the number of queries (1000). This gives you a time-per-query, which should be expressed in milliseconds. The python `perf_counter` routine from the [`time` module](https://docs.python.org/3/library/time.html) makes it easy to conduct such timing tests. We measure multiple queries because each query is fairly short and we want to average over many such queries.