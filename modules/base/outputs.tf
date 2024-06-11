output "redis_endpoint" {
    value = module.redis.redis_endpoint
}

output "s3_bucket_name" {
    value = module.s3_bucket.bucket_name
}

output "role_arn" {
    value = module.role.role_arn
}
