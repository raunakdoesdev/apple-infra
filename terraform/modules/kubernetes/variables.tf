variable "vpc_id" {
  type = string
}

variable "subnet_ids" {
  type = list(string)
}

variable "policy_arn" {
    type = string
    description = "iam policy arn"
}