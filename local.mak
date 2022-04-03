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
	# $(KC) apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.1.2/deploy/static/provider/cloud/deploy.yaml

deploy: k8s-components model-services pdf-text search-apis search-frontend
	$(KC) apply -f deploy/rabbitmq.yaml
	$(KC) apply -f deploy/model-services.yaml
	$(KC) apply -f deploy/pdf-text.yaml
	$(KC) apply -f deploy/search-apis.yaml
	$(KC) apply -f deploy/search-frontend.yaml

apply: k8s-components
	$(KC) apply -f deploy/ingress.yaml
	$(KC) apply -f deploy/rabbitmq.yaml
	$(KC) apply -f deploy/model-services.yaml
	$(KC) apply -f deploy/pdf-text.yaml
	$(KC) apply -f deploy/search-apis.yaml
	$(KC) apply -f deploy/search-frontend.yaml

scratch:
	$(KC) delete deploy --all