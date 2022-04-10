# search-services

## Repository Structure
- `deploy/` - Contains yaml files that describe deployment configuration
- `modal_playground/` - Contains various tests conducted in the model development stage as a note
- `model-services/` - The component that convert plain text research papers into features and predictions for the use of later stages of the pipeline
- `pdf-text/` - The component that convert PDF files to plain text. It is a wrapper around the repository [PDFBoT](https://github.com/yuchangfeng/PDFBoT), turning it into a microservice.
-  `search-apis/` - Backend API server for the search functionalities.
-  `search-frontend/` - Frontend React server that serves the webpages for the search engine.

## Acknowledgement
The core functionality of the PDF plaintext conversion component is built on top of [PDFBoT](https://github.com/yuchangfeng/PDFBoT), which in turn is derived from the paper written by [Yu, Changfeng, Cheng Zhang and Jie Wang. “Extracting Body Text from Academic PDF Documents for Text Mining.” KDIR (2020).](https://doi.org/10.48550/arXiv.2010.12647)

## To run the services locally
1. Make sure to have Docker and Minikube installed
2. From root directory, run `make -f local.mak deploy`
3. Run `minikube tunnel`, and the application would be accessible from `127.0.0.1`.

## To run the services on AWS EKS
### Prerequisites
1. AWS CLI correctly set-up with an AWS Account
2. `kubectl`
3. `eskctl`
4. Docker
5. Public Docker Image repositories
6. GNU `make`
### To run the services on EKS
1. Create four public Docker Image repository named `model-services`, `pdf-text`, `search-apis`, and `search-frontend`.
2. Copy all the files with `.template` file extension, and delete that extension. 
3. Fill in the `REGID` in `k8s.mak` with your DockerHub ID, and replace `DOCKER_IMAGE_IN_YOUR_REPOSITORY` in the four `.yaml` files derived from the `.template` files in `deploy/cloud/`.
4. Switch the working directory to the project root directory. 
5. Run `make -f eks.mak start` to start a EKS cluster. The configuration of the cluster could be changed in `eks.mak`.
6. Run `make -f k8s.mak deploy` to build, push and deploy the Docker images into the EKS cluster.
7. Run `kubectl get ingress` to find the public IP of the server.
### To operate the EKS cluster
Run `make -f eks.mak up` or `down` to start or stop the worker nodes, and use `make -f eks.mak stop` to delete the cluster completely

## To modify the images and deploy them
Make changes to the source files, and run `make -f k8s.mak SERVICE_NAME` to rebuild the Docker image, then `make -f k8s.mak scratch` and `make -f k8s.mak apply` to rollout the changes. The same could be done in local environment using `local.mak`