terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.2.0"
}

provider "aws" {
  region = var.aws_region
}

# VPC Configuration
resource "aws_vpc" "mongodb_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "mongodb-vpc"
  }
}

# Public Subnet
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.mongodb_vpc.id
  cidr_block              = var.public_subnet_cidr
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true

  tags = {
    Name = "mongodb-public-subnet"
  }
}

# Security Group for MongoDB
resource "aws_security_group" "mongodb_sg" {
  name        = "mongodb-security-group"
  description = "Security group for MongoDB cluster"
  vpc_id      = aws_vpc.mongodb_vpc.id

  ingress {
    from_port   = 27017
    to_port     = 27017
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

  tags = {
    Name = "mongodb-security-group"
  }
}

# EC2 Instance for MongoDB
resource "aws_instance" "mongodb_instance" {
  count                  = var.instance_count
  ami                    = var.ami_id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public_subnet.id
  vpc_security_group_ids = [aws_security_group.mongodb_sg.id]
  key_name              = var.key_name

  user_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get install -y mongodb
              systemctl start mongodb
              systemctl enable mongodb
              EOF

  tags = {
    Name = "mongodb-${count.index + 1}"
  }
} 