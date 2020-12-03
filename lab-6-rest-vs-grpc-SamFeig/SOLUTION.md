
|  Method 	| Local  	| Same-Zone  	|  SameReg/Diff Zone 	| Europe |
|---------- |---------- |-------------- |-----------------------|--------|
|   REST add|   3.26	|   	4.098	|  			3.33		|	280.78	|
|   gRPC add|   0.53	|   	0.73	|    		0.696		|	139.95	|
|   REST img|   4.60	|   	13.71	|   		13.589		|	1149.64	|
|   gRPC img|   7.23 	|   	13.86	|   		13.66		|	181.65	|
|   PING    |   0.045  	|   	0.292   |   		0.344    	|	138.48	|

The REST and the gRPC service for both `add` and `image` were run for an iteration count of 1000 for the first 3 tests.
For test 4, both services were run with an iteration count of 100.


## Results: ##

### Local - Test 1 ###

The gRPC service was roughly 5-6 times faster using REST for the add service on the local machine. This could be mainly due to the use of HTTP/2 by gRPC which is more efficient than REST's HTTP. Also gRPC is designed for low latency and high throughput and is best suited for low-weight services like the add function.

gRPC had significantly poorer performance than REST in terms of streaming data in the image test. Since both the client and server are running on the same host, REST communication doesn't have to be serialised. gRPC always serialises data even on the local network and so takes much more time.

### Same-Zone - Test 2 ###

When on two difference hosts that are within the same zone, the REST add services takes around 4.1 ms and the gRPC add service is about 5 times faster similar to test1. Both the REST and the gRPC add/image service take more than in the first test. This could be due to the fact that the client and server are running on two different machines and network latency depends on the pysical distance between the server and client, therefore meaning all of these are subject to higher network latency now that they are running on seperate machines.

The REST image and the gRPC image services take similar time for the queries. gRPC is not very good for streaming large data but REST doesn't significantly perform better despite this limitation. This is all likely due to the physical distance the packet needs to travel from source to destination between the seperate machines now.


### Same-Reg/Diff-Zone - Test 3 ###

The data from the same-region different-zone test is almost identical to the same-zone data from test 2. This is likely because once the data is leaving the zone, it is just about the same network latency to get to any of the other US zones within the region and all other performance is drowned out a bit. They are all relatively close together and connected by high speed networks across the US so it makes sense that data within the same region would be about as fast as data in any single zone as well since data anywhere in the US is pretty fast.


### Europe - Test 4 ###

When on a server in an entirely different zone (Europe), the REST services for both add and image perform very badly. This is due to the fact the REST service creates a new TCP connection for every request. If several network hops are needed before reaching the europe-west3 region, it will take a lot more time to complete. Network latency is dependent on the number of network devices which have to be crossed by a packet and so it is reasonable that moving to a different region/continent will make this number be much larger and so increase latency.

gRPC also takes large amounts of time per query but is also significantly better when compared to REST. REST and gRPC are closer in time for the add service but gRPC is almost as good as the direct PING where REST is much higher still. For the image service, REST is extremely poor coming in at over 1000 ms. gRPC only makes a single TCP connection from client to server which is used for all its queries and so can make better use of server resources than REST can which helps improves performance. gRPC is very fast due to the protocol buffers allowing for information to travel faster.

From these tests, gRPC is notably faster in every occurance excdept for streaming data across local regions (in which it performs just as well as REST) and so is the better choice of protocol to use. Especially if the data is moving across large network distances and back.


### Ping Results: ###
Measured using: `ping -c 100 10.xxx.x.x`

The average round trip time for the local machine is 0.045 ms
The average round trip time for the same zone machine is 0.292 ms
The average round trip time for the same region different zone machine is 0.344 ms
(Test 2 and test 3 ping show that the move to different machines is a larger latency jump than any move within a region due to the requirement to now use the external network. Once you are using the network, everything within a region will have just about the same network latency to get to eachother.)

The average round trip time for the Europe machine is 138.48 ms

The first 3 cases are all about the same because they are close together geographically. The Europe machine has a much higher latency because it is in two different regions and very far away so must make many more network hops to find its destination. 