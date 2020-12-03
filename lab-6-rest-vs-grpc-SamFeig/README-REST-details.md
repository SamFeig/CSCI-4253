# Rest Server Implementation

The REST server sample code is based on the Flask web framework.

You've installed Flask in lab5, but in this lab, you're going to extend the provided Flask server. If you want a "I just want to make it work" introduction, [this tutorial on Flask routes](https://hackersandslackers.com/the-art-of-building-flask-routes/) is good. There are official [flask tutorials](https://flask.palletsprojects.com/en/1.1.x/tutorial/) that provide more details.

You're being provided with a starting flask servers in `rest-server.py` that provides the basics of the specifics of extracting an image file over REST was devised from [an example here](https://gist.github.com/kylehounslow/767fb72fde2ebdd010a0bf4242371594). You'll need to add the `/api/add` method.

You need to provide an additional endpoint `/api/add/X/Y` that is a `POST` or `GET` method that returns a response with a JSON body containing the sum of the `X` and `Y` parameters. The body of the request is ignored.

We've provided starter code in `rest-client.py` that should construct a REST request for the `/api/image` queries. The image query loads a 1.6MB JPG image of the flatirons for processing. The image is from Wikipedia and taken by Jesse Varner. Modified by AzaToth. - Self-made photo.Originally uploaded on 2006-04-19 by Molas. Uploaded edit 2007-12-23 by AzaToth., CC BY-SA 2.5, https://commons.wikimedia.org/w/index.php?curid=3267545.

You will need to install the base Python3 system as well as the libraries `jsonpickle` and`Pillow` libraries in addition to the `Flask` libraries. The easiest way to do this is using the `pip` command.

You'll also need to add support for taking the IP address from the command line and running a test (either an `add` or `image` test) a certain number of times. You should get things working on one host first and then move it to the cloud.

You'll need to install some Python libraries in addition to the flask libraries installed in lab5. This command install the stuff I needed:
```
sudo pip3 install pillow jsonpickle flask
```

#### What you need to do for the Python section

You should modify the client and server to implement the `/api/add` method and insure that the sample client code receives the correct answer(s).

You should then modify the client to accept a command-line argument indicating the endpoint to be tested and the number of iterations to test. For example:
```
python rest-client.py localhost add 1000
```
would run the `/api/add` endpoint 1000 times against the server on the `localhost` and then report the time taken divided by the number of queries (1000). This gives you a time-per-query, which should be expressed in milliseconds. The python `perf_counter` routine from the [`time` module](https://docs.python.org/3/library/time.html) makes it easy to conduct such timing tests. We measure multiple queries because each query is fairly short and we want to average over many such queries.