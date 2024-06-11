variable "vpc_id" {
  type = string
  default = "vpc-0815f0dabd68edf17"
}

variable "subnet_ids" {
  type = list(string)
  default = [ "subnet-00a5188f9889e32d6", "subnet-03c68312710fc39b4", "subnet-0782f8a7b340eec4b" ]
}