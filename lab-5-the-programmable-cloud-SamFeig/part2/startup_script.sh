# Now run the flask application
cd /flask/examples/tutorial
export FLASK_APP=flaskr
export FLASK_ENV=development
flask init-db
nohup flask run -h 0.0.0.0 &
