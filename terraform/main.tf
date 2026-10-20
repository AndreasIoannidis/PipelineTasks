# Pin Terraform and the AWS provider to a recent 5.x release.
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.100.0"
    }
  }
}

# Configure AWS for offline validation and planning only; never contact a real account.
provider "aws" {
  region     = var.region
  access_key = "placeholder-access-key"
  secret_key = "placeholder-secret-key"

  skip_credentials_validation = true
  skip_requesting_account_id  = true
  skip_metadata_api_check     = true
}

# Local demo S3 bucket used only as a Terraform example resource.
resource "aws_s3_bucket" "artifacts" {
  bucket = "task-api-artifacts"

  tags = {
    environment = "dev"
    project     = "task-api"
  }
}
