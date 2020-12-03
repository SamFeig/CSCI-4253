##
## You provide this to build your docker image
##

NS := samfeig
VERSION := latest

IMAGE_NAME := logs-server
CONTAINER_NAME := logs-server
IMAGE_NAME2 := rest-server
CONTAINER_NAME2 := rest-server

REDIS_HOST := redis	
RABBITMQ_HOST := rabbitmq

PORT := 5000


build: buildLogs buildRest

buildLogs:
	docker build -t $(NS)/$(IMAGE_NAME):$(VERSION) -f Dockerfile-logs .

buildRest:
	docker build -t $(NS)/$(IMAGE_NAME2):$(VERSION) -f Dockerfile-rest .

push: pushLogs pushRest

pushLogs:
	docker push $(NS)/$(IMAGE_NAME):$(VERSION)

pushRest:
	docker push $(NS)/$(IMAGE_NAME2):$(VERSION)

runLogs:
	docker run -e $(REDIST_HOST) -e $(RABBITMQ_HOST) $(NS)/$(IMAGE_NAME):$(VERSION)

runRest:
	docker run -e $(REDIST_HOST) -e $(RABBITMQ_HOST) -p $(PORT):$(PORT) $(NS)/$(IMAGE_NAME2):$(VERSION)

runKube:
	kubectl apply -f rest-deployment.yaml
	kubectl apply -f rest-service.yaml
	kubectl apply -f rest-ingress.yaml
	sleep 5
	@#kubectl port-forward --address 0.0.0.0 service/rest-service 5000:5000 &
	@#sleep 5
	kubectl apply -f logs-deployment.yaml	

cleanKube:
	kubectl delete deployment rest-server
	kubectl delete deployment logs-server
	kubectl delete service rest-service
	kubectl delete ingress rest-ingress
	-@#pkill -f port-forward

default: build