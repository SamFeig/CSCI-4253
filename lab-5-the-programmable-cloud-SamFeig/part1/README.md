# Part One - Program to Create a VM and install an Application

In this part, you're going to write a simple program to create a VM install the [flask tutorial application](https://github.com/pallets/flask/tree/master/examples/tutorial). In later labs, we'll be using [Flask](https://palletsprojects.com/p/flask/) to write a simple REST interface.

Before starting this lab, [you should go through every step of the Google cloud Python tutorial](https://cloud.google.com/compute/docs/tutorials/python-guide). It is very important that you run the command
```
gcloud auth application-default login
```
if you're using your laptop. This command authenticates you to Google cloud and stores the credentials in your home directory. This is done automatically if you're using Google Cloud.

You should [clone the programming tutorial from github](https://github.com/GoogleCloudPlatform/python-docs-samples) and run the code examples in `compute/api/create_instance.py`. You will be able to borrow liberally from this code for your assignment (giving proper attribution, of course).

The tutorial goes through the steps of creating an instance. That instance is created using a `debian-9` image. As part of the startup code for that image, the `startup_script` shell script is executed; that script retrieves an image (specified by the program), modifies it and places it in a Google storage `bucket`.

Our program will be similar:
* You will create an image (the `f1-micro` image is "free") in the "us-west-1b" [zone](https://cloud.google.com/compute/docs/regions-zones/).
* You should use the `ubuntu-1804-lts` images from the `ubuntu-os-cloud` "family" of public images. This will start with a "Bionic Beaver" release. You can determine the avaialable versions using
```
gcloud compute images list | grep -i ubuntu
```
* You will use the `default` network and use the same `ONE_TO_ONE_NAT` option in the example
* In your startup script, you should `git clone` the [flask git repo](https://github.com/pallets/flask) and then install the `flaskr` application (see below)
* You should create a [firewall rule](https://cloud.google.com/vpc/docs/firewalls) called `allow-5000` using the [firewall API](https://cloud.google.com/compute/docs/reference/rest/v1/firewalls). You should allow TCP port `5000` to be accessed from anywhere (e.g. `0.0.0.0/0`). Note that you only need to create the firewall rule once, but you should do so from your code. You can check if the firewall rule exists by name using the [API](https://cloud.google.com/compute/docs/reference/rest/v1/firewalls/list). You should have the firewall rule use a "network tag" so that it applies only to instances with that tag. You can name that tag `allow-5000` as well.
* Then, apply the network tag `allow-5000` to your VM instance using [setTags](https://cloud.google.com/compute/docs/reference/rest/v1/instances/setTags).
* You should retrieve the public / external IP address from the instance information and invite the user to visit the appropriate url (e.g. http://35.197.100.174:5000 or whatever your IP address is)

To install the example flask application, you will need to install `python3` and `python3-pip`. Something like this should work:
```
sudo apt-get update
sudo apt-get install -y python3 python3-pip git
git clone https://github.com/pallets/flask
cd ~/flask/examples/tutorial
sudo python3 setup.py install
sudo pip3 install -e .
```
should build and install the software. To then run the application, you should specify:
```
export FLASK_APP=flaskr
flask init-db
nohup flask run -h 0.0.0.0 &
```
This last line starts the `flask` application and `nohup` insures that it continues to run after the `startup_script.sh` finishes execution.

## Recommendations

You should first perform each step manually using the google console.

If you're uncertain how to configure a certain option (e.g. a network tag or somesuch), you can configure it using the GUI and then run
```
gcloud compute instances list --format=json
```
to get a complete dump of the instance configuration details. This can help you narrow down what part of the API documentation to consult or determine valid values.
