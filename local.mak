DK=docker
ARCH=--platform x86_64
KC=kubectl

.PHONY: model-services 
model-services:
	$(DK) build $(ARCH) -t model-services model-services
	minikube cache delete model-services
	minikube cache add model-services

.PHONY: pdf-text
pdf-text:
	$(DK) build $(ARCH) -t pdf-text pdf-text
	minikube cache delete pdf-text
	minikube cache add pdf-text

.PHONY: search-apis
search-apis:
	$(DK) build $(ARCH) -t search-apis search-apis
	minikube cache delete search-apis
	minikube cache add search-apis

.PHONY: rabbitmq-operator
rabbitmq-operator:
	$(KC) apply -f "https://github.com/rabbitmq/cluster-operator/releases/latest/download/cluster-operator.yml"

deploy: rabbitmq-operator model-services pdf-text search-apis
	$(KC) apply -f deploy/rabbitmq.yaml
	$(KC) apply -f deploy/model-services.yaml
	$(KC) apply -f deploy/pdf-text.yaml
	$(KC) apply -f deploy/search-apis.yaml

apply:
	$(KC) apply -f deploy/rabbitmq.yaml
	$(KC) apply -f deploy/model-services.yaml
	$(KC) apply -f deploy/pdf-text.yaml
	$(KC) apply -f deploy/search-apis.yaml

scratch:
	$(KC) delete deploy --all