DK=docker
ARCH=--platform x86_64
KC=kubectl

.PHONY: model-services 
model-services:
	$(DK) build $(ARCH) -t model-services model-services
	-minikube cache delete model-services 2> /dev/null
	minikube cache add model-services

.PHONY: pdf-text
pdf-text:
	$(DK) build $(ARCH) -t pdf-text pdf-text
	-minikube cache delete pdf-text 2> /dev/null
	minikube cache add pdf-text

.PHONY: search-apis
search-apis:
	$(DK) build $(ARCH) -t search-apis search-apis
	-minikube cache delete search-apis 2> /dev/null
	minikube cache add search-apis

.PHONY: search-frontend
search-frontend:
	$(DK) build $(ARCH) -t search-frontend search-frontend
	-minikube cache delete search-frontend 2> /dev/null
	minikube cache add search-frontend

.PHONY: k8s-components
k8s-components:
	$(KC) apply -f "https://github.com/rabbitmq/cluster-operator/releases/latest/download/cluster-operator.yml"
	minikube addons enable ingress

.PHONY: redis
redis:
	$(KC) apply -f deploy/local/redis-config.yaml
	$(KC) apply -f deploy/local/redis.yaml

deploy: redis k8s-components model-services pdf-text search-apis search-frontend
	$(KC) apply -f deploy/local/ingress.yaml
	$(KC) apply -f deploy/local/rabbitmq.yaml
	$(KC) apply -f deploy/local/model-services.yaml
	$(KC) apply -f deploy/local/pdf-text.yaml
	$(KC) apply -f deploy/local/search-apis.yaml
	$(KC) apply -f deploy/local/search-frontend.yaml

apply: redis k8s-components
	$(KC) apply -f deploy/local/ingress.yaml
	$(KC) apply -f deploy/local/rabbitmq.yaml
	$(KC) apply -f deploy/local/model-services.yaml
	$(KC) apply -f deploy/local/pdf-text.yaml
	$(KC) apply -f deploy/local/search-apis.yaml
	$(KC) apply -f deploy/local/search-frontend.yaml

scratch:
	$(KC) delete deploy --all