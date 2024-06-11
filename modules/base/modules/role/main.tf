resource "aws_iam_role" "reducto_container_role" {
  name_prefix = "reducto-container-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

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

resource "aws_iam_role_policy_attachment" "reducto_container_policy_attachment" {
  role       = aws_iam_role.reducto_container_role.name
  policy_arn = aws_iam_policy.reducto_container_policy.arn
}

variable "bucket_name" {
  type = string
}

output "role_arn" {
  value = aws_iam_role.reducto_container_role.arn
}
