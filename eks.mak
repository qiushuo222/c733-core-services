REGION=us-west-2
CONTEXT_NAME=search-context
NODE_TYPE=c6g.2xlarge
NUM_NODES=5

start: 
	eksctl create cluster --name search-cluster --version 1.21 --region $(REGION) --nodegroup-name search-worker-nodes --node-type $(NODE_TYPE) --nodes $(NUM_NODES) --nodes-min $(NUM_NODES) --nodes-max $(NUM_NODES) --managed
	kubectl config rename-context `kubectl config current-context` $(CONTEXT_NAME)

stop:
	eksctl delete cluster --name search-cluster --region $(REGION)
	kubectl config delete-context $(CONTEXT_NAME)

up:
	eksctl create nodegroup --cluster search-cluster --region $(REGION) --name search-worker-nodes --node-type $(NODE_TYPE) --nodes $(NUM_NODES) --nodes-min $(NUM_NODES) --nodes-min $(NUM_NODES) --managed

down:
	eksctl delete nodegroup --cluster=search-cluster --region $(REGION) --name=search-worker-nodes