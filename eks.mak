REGION=us-west-2
CONTEXT_NAME=search-context
NODE_TYPE=t3.medium

start: 
	eksctl create cluster --name search-cluster --version 1.21 --region $(REGION) --nodegroup-name search-worker-nodes --node-type $(NODE_TYPE) --nodes 2 --nodes-min 2 --nodes-max 2 --managed
	kubectl config rename-context `kubectl config current-context` $(CONTEXT_NAME)

stop:
	eksctl delete cluster --name search-cluster --region $(REGION)
	kubectl config delete-context $(CONTEXT_NAME)

up:
	eksctl create nodegroup --cluster search-cluster --region $(REGION) --name search-worker-nodes --node-type $(NTYPE) --nodes 2 --nodes-min 2 --nodes-min 2 --managed

down:
	eksctl delete nodegroup --cluster=search-cluster --region $(REGION) --name=search-worker-nodes