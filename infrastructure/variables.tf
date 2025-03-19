variable "region" {
  default = "us-east-1"
}

variable "ecr_repo_name" {
  default = "visa-pred-repo"
}

variable "github_owner" {
  description = "GitHub owner/organization"
  type        = string
}

variable "github_repo" {
  description = "GitHub repository name"
  type        = string
}

variable "github_token" {
  description = "GitHub personal access token"
  type        = string
  sensitive   = true
}