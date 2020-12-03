##
## You provide this to build your docker image
##

NS := samfeig
VERSION := latest

IMAGE_NAME := worker-server
CONTAINER_NAME := worker-server

REDIS_HOST := redis	
RABBITMQ_HOST := rabbitmq

PORT := 5000


build:
	docker build -t $(NS)/$(IMAGE_NAME):$(VERSION) -f Dockerfile-worker .

push:
	docker push $(NS)/$(IMAGE_NAME):$(VERSION)

run:
	docker run -e $(REDIST_HOST) -e $(RABBITMQ_HOST) -p $(PORT):$(PORT) $(NS)/$(IMAGE_NAME):$(VERSION)

runKube:
	kubectl apply -f worker-deployment.yaml

cleanKube:
	kubectl delete deployment worker-server

default: build