variable "vpc_id" {
  type = string
}

variable "subnet_ids" {
  type = list(string)
}

variable "boundary_policy_arn" {
  type = string
}
