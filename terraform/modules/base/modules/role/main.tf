resource "aws_iam_policy" "reducto_container_policy" {
  name_prefix = "reducto-container-policy"
  description = "IAM policy to allow access to s3 and textract"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:*",
        ]
        Resource = [
          "arn:aws:s3:::${var.bucket_name}/*",
          "arn:aws:s3:::${var.bucket_name}"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "textract:DetectDocumentText",
        ]
        Resource = "*"
      }
    ]
  })
}


variable "bucket_name" {
  type = string
}

output "policy_arn" {
  value = aws_iam_policy.reducto_container_policy.arn
}
