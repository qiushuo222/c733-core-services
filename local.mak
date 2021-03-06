ARCH=--platform x86_64

.PHONY: model-services 
model-services:
	docker build $(ARCH) -t model-services model-services
	-minikube cache delete model-services 2> /dev/null
	minikube cache add model-services

.PHONY: pdf-text
pdf-text:
	docker build $(ARCH) -t pdf-text pdf-text
	-minikube cache delete pdf-text 2> /dev/null
	minikube cache add pdf-text

.PHONY: search-apis
search-apis:
	docker build $(ARCH) -t search-apis search-apis
	-minikube cache delete search-apis 2> /dev/null
	minikube cache add search-apis

.PHONY: search-frontend
search-frontend:
	docker build $(ARCH) -t search-frontend search-frontend
	-minikube cache delete search-frontend 2> /dev/null
	minikube cache add search-frontend

.PHONY: k8s-components
k8s-components:
	kubectl apply -f "https://github.com/rabbitmq/cluster-operator/releases/latest/download/cluster-operator.yml"
	minikube addons enable ingress

.PHONY: redis
redis:
	kubectl apply -f deploy/local/redis-config.yaml
	kubectl apply -f deploy/local/redis.yaml

deploy: redis k8s-components model-services pdf-text search-apis search-frontend
	kubectl apply -f deploy/local/ingress.yaml
	kubectl apply -f deploy/local/rabbitmq.yaml
	kubectl apply -f deploy/local/model-services.yaml
	kubectl apply -f deploy/local/pdf-text.yaml
	kubectl apply -f deploy/local/search-apis.yaml
	kubectl apply -f deploy/local/search-frontend.yaml

apply: redis k8s-components
	kubectl apply -f deploy/local/ingress.yaml
	kubectl apply -f deploy/local/rabbitmq.yaml
	kubectl apply -f deploy/local/model-services.yaml
	kubectl apply -f deploy/local/pdf-text.yaml
	kubectl apply -f deploy/local/search-apis.yaml
	kubectl apply -f deploy/local/search-frontend.yaml

scratch:
	kubectl delete deploy --all