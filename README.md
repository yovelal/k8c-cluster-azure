# k8c-cluster-azure

## Prerequisites
Before you start, ensure you have the following tools installed:
- Terraform
- Helm
- kubectl
- An active Azure account

## Introduction
`k8c-cluster-azure` is a project designed to deploy Kubernetes clusters on Azure with ease and efficiency. 
It utilizes Helm charts for easy and consistent application deployment and management within the Kubernetes cluster.


## Installation
# create the cluster
1. Login to Azure CLI: az login
2. Change directory to the Terraform configuration:cd terraform
3. (Optional) Preview the Terraform plan: terraform plan
4. Apply the Terraform configuration: terraform apply
5. Retrieve credentials for the Kubernetes cluster: az aks get-credentials --name my-cluster --resource-group home-assignment
   Note: At this point, your cluster and resource group should be visible in the Azure portal.
7. (Optional) Verify the current context is set to the new cluster: kubectl config current-context
8. Return to the previous directory:cd ..

# install the chart
1. Apply the Kubernetes Ingress NGINX controller: kubkubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yamlectl 
2. Install the Helm chart: helm install releaset ./chart

## Access the apps
1. Retrieve the IP address for accessing the applications: kubectl get ingress -n namespace1
   The IP address is located in the "ADDRESS" field.
2. You can access the applications through: `http://<ip>/service-a` and `http://<ip>/service-b`


![image](https://github.com/yovelal/k8c-cluster-azure/assets/100790447/16f2c901-1ea2-4699-8ac8-7b089da0647e)


