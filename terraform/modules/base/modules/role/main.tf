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
        ],
        Condition = {
          StringEquals = {
            "iam:PermissionsBoundary" = var.boundary_policy_arn
          }
        }
      },
      {
        Effect = "Allow"
        Action = [
          "textract:DetectDocumentText",
        ]
        Resource = "*"
        Condition = {
          StringEquals = {
            "iam:PermissionsBoundary" = var.boundary_policy_arn
          }
        }
      }
    ]
  })
}


variable "bucket_name" {
  type = string
}

variable "boundary_policy_arn" {
  type = string
}

output "policy_arn" {
  value = aws_iam_policy.reducto_container_policy.arn
}
