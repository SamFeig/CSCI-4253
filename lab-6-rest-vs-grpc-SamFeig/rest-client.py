#!/usr/bin/env python3
from __future__ import print_function
import requests
import json
import sys
from time import perf_counter

if len(sys.argv) != 4:
    print("\npython rest-client.py <server address> <endpoint> <iterations>")
    exit()

addr = 'http://' + sys.argv[1] + ':5000'

endpoint = sys.argv[2]
num_iterations = sys.argv[3]
n = int(num_iterations)

# prepare headers for http request
headers = {'content-type': 'image/png'}
headers1 = {'content-type': 'text/plain'}

img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()

# send http request with image and receive response
image_url = addr + '/api/image'
number_url = addr + '/api/add/2/3'

#Image service
if(endpoint == 'image'):
    count = 1
    start = perf_counter()

    while(count <= n): 
        response = requests.post(image_url, data=img, headers=headers)
        print("Response is", response)
        print(json.loads(response.text))
        count += 1

    total_time = perf_counter() - start
    print(str(total_time/n * 1000) + ' ms')

#Add service
else:
    count = 1
    start = perf_counter()

    while(count <= n): 
        response1 = requests.get(number_url, headers=headers1)
        print("Response is", response1)
        print(json.loads(response1.text))
        count = count+1

    total_time = perf_counter() - start
    print(str(total_time/n * 1000) + ' ms')
