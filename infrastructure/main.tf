provider "aws" {
  region = var.region
}

# Create IAM user for GitHub Actions
resource "aws_iam_user" "github_user" {
  name = "github-actions-user"
}

resource "aws_iam_access_key" "github_key" {
  user = aws_iam_user.github_user.name
}

# Attach ECR permissions
resource "aws_iam_user_policy_attachment" "ecr_access" {
  user       = aws_iam_user.github_user.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser"
}

# Create ECR Repository
resource "aws_ecr_repository" "app_repo" {
  name = var.ecr_repo_name
}

# Create EC2 Security Group
resource "aws_security_group" "app_sg" {
  name        = "app-security-group"
  description = "Allow web and SSH access"

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create SSH Key
resource "tls_private_key" "ssh_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "deploy_key" {
  key_name   = "ec2-deploy-key"
  public_key = tls_private_key.ssh_key.public_key_openssh
}

# Create EC2 Instance
data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_instance" "app_server" {
  ami             = data.aws_ami.ubuntu.id
  instance_type   = "t2.medium"
  key_name        = aws_key_pair.deploy_key.key_name
  security_groups = [aws_security_group.app_sg.name]

  user_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get install -y docker.io
              systemctl start docker
              systemctl enable docker
              usermod -aG docker ubuntu
              EOF

  tags = {
    Name = "VisaPredictionServer"
  }
}