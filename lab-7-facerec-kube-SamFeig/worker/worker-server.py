#
# Worker server
#
import jsonpickle, pickle
import platform
from PIL import Image
import io
import os
import sys
import pika
import redis
import hashlib
import face_recognition
import json

hostname = platform.node()

##
## Configure test vs. production
##
redisHost = os.getenv("REDIS_HOST") or "localhost"
rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"

print("Connecting to rabbitmq({}) and redis({})".format(rabbitMQHost,redisHost))

##
## You provide this
##

redisNameToHash = redis.Redis(host=redisHost, db=1, decode_responses=True)    # Key -> Value
redisHashToName = redis.Redis(host=redisHost, db=2, decode_responses=True)    # Key -> Set
redisHashToFaceRec = redis.Redis(host=redisHost, db=3, decode_responses=True) # Key -> Set
redisHashToHashSet = redis.Redis(host=redisHost, db=4, decode_responses=True) # Key -> Set

def log(message, debug=False):
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitMQHost))
    channel = connection.channel()
    channel.exchange_declare(exchange='logs', exchange_type='topic')

    routing_key = '%s.rest.%s'% (rabbitMQHost, 'debug' if debug else 'info')
    channel.basic_publish(exchange='logs', routing_key=routing_key, body=message)
    print(" [x] Sent %r:%r" % (routing_key, message))
    channel.close()
    connection.close()

def callback(ch, method, properties, body):
    #data = body.decode()
    data = jsonpickle.decode(body)
    print(" [x] Received %r" % data)


    hash = data['hash']
    name = data['name']
    rawImage = data['image']

    #Add to DBs
    redisNameToHash.set(name, hash)
    log("Added (%s, %s) to redisNameToHash" % (name, hash))
    redisHashToName.sadd(hash, name)
    log("Added (%s, %s) to redisHashToName" % (hash, name))        

    #If image not processed, process it
    if(len(redisHashToFaceRec.lrange(hash, 0, -1)) == 0):
        img = face_recognition.load_image_file(io.BytesIO(rawImage))
        # Get face encodings for any faces in the uploaded image
        unknown_face_encodings = face_recognition.face_encodings(img)
        log("Face Encoding: %r" % (unknown_face_encodings), True)
        
        if(len(unknown_face_encodings) > 0):
            #Add FaceRec data to redis list
            for face in unknown_face_encodings:
                for value in face:
                    redisHashToFaceRec.rpush(hash, value)
            log("Added Face Encoding for %s to redisHashToFaceRec" % (hash))

            for face in redisHashToFaceRec.keys():
                if face != hash:
                    known_face_encoding = [float(i) for i in redisHashToFaceRec.lrange(face, 0, -1)]
                    
                    if face_recognition.compare_faces([known_face_encoding], unknown_face_encodings[0])[0]:
                        for val in redisHashToName.smembers(face):
                            redisHashToHashSet.sadd(hash, val)
                            log("Added (%s, %s) to redisHashToHashSet" % (hash, val))
                        for val in redisHashToName.smembers(hash):
                            redisHashToHashSet.sadd(face, val)
                            log("Added (%s, %s) to redisHashToHashSet" % (face, val))

    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitMQHost))
channel = connection.channel()

channel.queue_declare(queue='toWorker', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='toWorker', on_message_callback=callback)

channel.start_consuming()

