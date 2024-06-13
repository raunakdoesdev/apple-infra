
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
  boundary_policy_arn = var.boundary_policy.arn
}
