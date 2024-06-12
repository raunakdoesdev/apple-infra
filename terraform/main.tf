provider "aws" {
  region  = "us-west-2"  # You can change the region as needed
}

module "base" {
  source = "./modules/base"
  vpc_id = var.vpc_id
  subnet_ids = var.subnet_ids
}

module "kubernetes" {
    source = "./modules/kubernetes"
    vpc_id = var.vpc_id
    subnet_ids = var.subnet_ids
}


module "helm" {
    source = "./modules/helm"
    eks_cluster_name = module.kubernetes.cluster_name
}


output "nginx_endpoint" {
    value = module.helm.nginx_endpoint
}