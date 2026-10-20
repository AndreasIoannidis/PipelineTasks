# Export the planned bucket name so it can be inspected after a plan.
output "bucket_name" {
  description = "Name of the artifacts S3 bucket."
  value       = aws_s3_bucket.artifacts.bucket
}
