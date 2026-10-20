# Region the AWS provider would use; default is us-east-1.
variable "region" {
  type        = string
  description = "AWS region for planning this configuration."
  default     = "us-east-1"
}
