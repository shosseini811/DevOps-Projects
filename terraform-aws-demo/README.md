# Simple AWS Infrastructure with Terraform

This project demonstrates how to create a basic AWS infrastructure using Terraform. It sets up:
- A VPC with a public subnet
- An Internet Gateway
- A Route Table
- A Security Group allowing SSH access
- An EC2 instance running Amazon Linux 2

## Prerequisites

1. [Terraform](https://www.terraform.io/downloads.html) installed
2. AWS account and [AWS CLI](https://aws.amazon.com/cli/) configured
3. AWS credentials configured (`aws configure`)

## Usage

1. Initialize Terraform:
```bash
terraform init
```

2. Review the planned changes:
```bash
terraform plan
```

3. Apply the configuration:
```bash
terraform apply
```

4. To destroy the infrastructure:
```bash
terraform destroy
```

## Variables

You can customize the deployment by modifying the variables in `variables.tf` or by creating a `terraform.tfvars` file.

## Outputs

After successful deployment, Terraform will output:
- Public IP of the EC2 instance
- VPC ID
- Public Subnet ID

## Security Note

The security group allows SSH access from any IP (0.0.0.0/0). For production use, please restrict this to your specific IP range.
