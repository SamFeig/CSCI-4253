##
from flask import Flask, request, Response
import jsonpickle, pickle
import platform
import io, os, sys
import pika, redis
import hashlib, requests

##
## Configure test vs. production
##
redisHost = os.getenv("REDIS_HOST") or "localhost"
rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"

print("Connecting to rabbitmq({}) and redis({})".format(rabbitMQHost,redisHost))

# Initialize the Flask application
app = Flask(__name__)

##
## You provide this
##
def log(message, debug=False):
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitMQHost))
    channel = connection.channel()
    channel.exchange_declare(exchange='logs', exchange_type='topic')

    routing_key = '%s.rest.%s'% (rabbitMQHost, 'debug' if debug else 'info')
    channel.basic_publish(exchange='logs', routing_key=routing_key, body=message)
    print(" [x] Sent %r:%r" % (routing_key, message))
    channel.close()
    connection.close()
    

def sendToWorker(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitMQHost))
    channel = connection.channel()
    channel.queue_declare(queue='topic', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key = 'toWorker',
        body=jsonpickle.encode(message),
        properties=pika.BasicProperties(delivery_mode=2))
    channel.close()
    connection.close()

@app.route('/', methods=['GET'])
def hello():
    return '<h1> Face Rec Server</h1><p> Use a valid endpoint </p>'

@app.route('/scan/image/<filename>' , methods=['POST'])
def scanImage(filename):
    log("Attempting API request on /scan/image/%s" % (filename), True)

    image = request.data
    m = hashlib.sha256()
    m.update(image)

    response = { 
        "hash" : m.hexdigest()
    }
    response_pickled = jsonpickle.encode(response)
    sendToWorker({ 'hash' : m.hexdigest(), 'name' : filename, 'image' : image})

    log('POST /scan/image/%s HTTP/1.1 200' % (filename) , True)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/scan/url' , methods=['POST'])
def scanURL():
    url = request.get_json()['url']
    log("Attempting API request on /scan/url %s" % (url), True)
    
    image = requests.get(url, allow_redirects=True)
    m = hashlib.sha256()
    m.update(image.content)

    response = { 
        "hash" : m.hexdigest()
    }
    response_pickled = jsonpickle.encode(response)
    sendToWorker({ 'hash' : m.hexdigest(), 'name' : url, 'image' : image.content})

    log('POST /scan/url/ %s HTTP/1.1 200' % (url), True)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/match/<hash>' , methods=['GET'])
def matchHash(hash):
    redisHashToHashSet = redis.Redis(host=redisHost, db=4, decode_responses=True)

    response = { 
        "match" : list(redisHashToHashSet.smembers(hash))
    }

    response_pickled = jsonpickle.encode(response)

    log('GET /match/%s HTTP/1.1 200' % (hash), True)
    return Response(response=response_pickled, status=200, mimetype="application/json")


# start flask app
app.run(host="0.0.0.0", port=5000)
