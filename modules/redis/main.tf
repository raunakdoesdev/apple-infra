resource "aws_elasticache_subnet_group" "redis_subnet_group" {
  name       = "my-redis-subnet-group"
  subnet_ids = var.subnet_ids
}

#
resource "aws_elasticache_serverless_cache" "reducto-elasticache" {
  name   = "reducto-redis-serverless"
  engine = "redis"
  major_engine_version     = "7"
  security_group_ids       = [aws_security_group.redis_security_group.id]
  subnet_ids               = var.subnet_ids
}

resource "aws_security_group" "redis_security_group" {
  name_prefix = "redis-security-group"
  description = "Security group for Redis ElastiCache"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 6379
    to_port     = 6379
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}



variable "vpc_id" {
  type = string
}

variable "subnet_ids" {
  type = list(string)
}

output "redis_endpoint" {
    value = "${aws_elasticache_serverless_cache.reducto-elasticache.endpoint[0].address}:${aws_elasticache_serverless_cache.reducto-elasticache.endpoint[0].port}"
}
