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
