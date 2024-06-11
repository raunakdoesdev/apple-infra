resource "aws_s3_bucket" "bucket" {
    bucket_prefix = "reducto-bucket"
}

resource "aws_s3_bucket_lifecycle_configuration" "example" {
  bucket = aws_s3_bucket.bucket.id

  rule {
    id     = "expire-1d"
    status = "Enabled"
    expiration {
      days = 1
    }
  }
}


output "bucket_name" {
    value = aws_s3_bucket.bucket.bucket
}