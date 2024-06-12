output "redis_endpoint" {
    value = module.redis.redis_endpoint
}

output "s3_bucket_name" {
    value = module.s3_bucket.bucket_name
}

output "policy_arn" {
    value = module.role.policy_arn
}
