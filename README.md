## Apple Basic Resources

This Terraform module sets up basic AWS resources required for an application. Here's a breakdown of what the module does:

1. **Provider Configuration**:
   - Configures the AWS provider to use the `us-west-2` region.

2. **Modules**:
   - **Redis Module**: Sets up a Redis instance using the provided VPC ID and subnet IDs.
   - **S3 Bucket Module**: Creates an S3 bucket.
   - **Role Module**: Creates an IAM role with permissions to access the S3 bucket and use AWS Textract. The S3 bucket name is passed from the S3 bucket module to the role module.

3. **Variables**:
   - `vpc_id`: A string variable that holds the VPC ID, with a default value.
   - `subnet_ids`: A list of strings variable that holds the subnet IDs, with default values provided.

4. **Outputs**:
   - `redis_endpoint`: Outputs the Redis endpoint.
   - `s3_bucket_name`: Outputs the S3 bucket name.
   - `role_arn`: Outputs the ARN of the IAM role.

This module orchestrates the creation and management of AWS resources by leveraging modular and reusable code blocks, making it easier to manage infrastructure as code.

