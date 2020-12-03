#!/usr/bin/env python3
##
## Sample Flask REST server implementing two methods
##
## Endpoint /api/image is a POST method taking a body containing an image
## It returns a JSON document providing the 'width' and 'height' of the
## image that was provided. The Python Image Library (pillow) is used to
## process the image
##
## Endpoint /api/add/X/Y is a post or get method returns a JSON body
## containing the sum of 'X' and 'Y'. The body of the request is ignored
##
##
from flask import Flask, request, Response
import jsonpickle
import numpy as np
from PIL import Image
import io

# Initialize the Flask application
app = Flask(__name__)


# route http posts to this method
@app.route('/api/image', methods=['POST'])
def test():
    r = request
    # convert the data to a PIL image type so we can extract dimensions
    try:
        ioBuffer = io.BytesIO(r.data)
        img = Image.open(ioBuffer)
    # build a response dict to send back to client
        response = {
            'width' : img.size[0],
            'height' : img.size[1]
            }
    except:
        response = { 'width' : 0, 'height' : 0}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

def add(X,Y):
    return (X+Y)

@app.route('/api/add/<int:X>/<int:Y>' , methods=['GET', 'POST'])
def test2(X,Y):
    r1 = request
    try:
        sum_numbers = add(X,Y)
        response1 = { 
            'sum' : sum_numbers
        }

    except:
        response1 ={
            'sum' : 0
        }

    response1_pickled = jsonpickle.encode(response1)

    return Response(response=response1_pickled, status=200, mimetype="application/json")


# start flask app
app.run(host="0.0.0.0", port=5000)