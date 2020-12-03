# Basic setup to install the flask application
sudo apt-get update
sudo apt-get install -y python3 python3-pip git
git clone https://github.com/pallets/flask
cd /flask/examples/tutorial
sudo python3 setup.py install
sudo pip3 install -e .

# Now run the flask application
export FLASK_APP=flaskr
export FLASK_ENV=development
flask init-db
nohup flask run -h 0.0.0.0 &
