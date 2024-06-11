provider "aws" {
  region  = "us-west-2"  # You can change the region as needed
}

module "redis" {
  source = "./modules/redis"
  vpc_id = var.vpc_id
  subnet_ids = var.subnet_ids
}

module "s3_bucket" {
  source = "./modules/s3"
}

module "role" {
  source = "./modules/role"
  bucket_name = module.s3_bucket.bucket_name
}

variable "vpc_id" {
  type = string
  default = "vpc-0815f0dabd68edf17"
}

variable "subnet_ids" {
  type = list(string)
  default = [ "subnet-00a5188f9889e32d6", "subnet-03c68312710fc39b4", "subnet-0782f8a7b340eec4b" ]
}

output "redis_endpoint" {
    value = module.redis.redis_endpoint
}

output "s3_bucket_name" {
    value = module.s3_bucket.bucket_name
}

output "role_arn" {
    value = module.role.role_arn
}
