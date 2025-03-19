output "ecr_repo_url" {
  value = aws_ecr_repository.app_repo.repository_url
}

output "aws_access_key" {
  value     = aws_iam_access_key.github_key.id
  sensitive = true
}

output "aws_secret_key" {
  value     = aws_iam_access_key.github_key.secret
  sensitive = true
}

output "ec2_public_ip" {
  value = aws_instance.app_server.public_ip
}

output "ssh_private_key" {
  value     = tls_private_key.ssh_key.private_key_pem
  sensitive = true
}