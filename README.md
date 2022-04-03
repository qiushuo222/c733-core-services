# search-services
## To run the services locally
1. Make sure to have Docker and Minikube installed
2. From root directory, run `make -f local.mak deploy`
3. Run `minikube tunnel`, and the application should appear on `127.0.0.1` in your browser.

## To run the services on AWS EKS
### Prerequisites
1. AWS EKS control