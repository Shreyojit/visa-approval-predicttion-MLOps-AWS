variable "aws_region" {
  description = "AWS deployment region"
  default     = "us-east-1"
}

variable "ecr_repo_name" {
  description = "ECR repository name"
  default     = "us-visa-classifier"
}

variable "s3_bucket_name" {
  description = "S3 bucket for model storage"
  default     = "us-visa-models-2023"
}

variable "ec2_instance_type" {
  description = "EC2 instance type"
  default     = "t3.medium"
}

variable "app_port" {
  description = "Application port"
  default     = 8080
}