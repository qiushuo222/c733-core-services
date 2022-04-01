ARCH=--platform x86_64
KC=kubectl
REPO=TO_BE_FILLED

.PHONY: docker-login
docker-login:
	docker registry login

.PHONY: model-services
model-services:
	docker build $(ARCH) -t $(REPO)/model-services model-services
	docker push $(REPO)/model-services

.PHONY: pdf-text
pdf-text:
	docker build $(ARCH) -t pdf-text pdf-text
	docker push $(REPO)/pdf-text

.PHONY: search-apis
search-apis:
	docker build $(ARCH) -t search-apis search-apis
	docker push $(REPO)/search-apis

rabbitmq-operator:
	$(KC) apply -f "https://github.com/rabbitmq/cluster-operator/releases/latest/download/cluster-operator.yml"

deploy: rabbitmq-operator model-services pdf-text search-apis
	$(KC) apply -f deploy/rabbitmq.yaml
	$(KC) apply -f deploy/model-services.yaml
	# $(KC) apply -f deploy/pdf-text.yaml
	# $(KC) apply -f deploy/search-apis.yaml

scratch:
	$(KC) delete deploy --all