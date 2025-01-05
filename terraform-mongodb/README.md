# Terraform MongoDB Cluster with Python Backend

This project provides an automated way to deploy a MongoDB cluster on AWS using Terraform, along with a Python FastAPI backend for interacting with the database.

## Prerequisites

- AWS Account and AWS CLI configured
- Terraform installed (v1.2.0 or later)
- Python 3.8 or later
- An SSH key pair in your AWS account
- Docker (for containerized deployment)

## Project Structure

```
terraform-mongodb/
├── main.tf              # Main Terraform configuration
├── variables.tf         # Terraform variables
├── backend/
│   ├── main.py         # Python FastAPI application
│   ├── Dockerfile      # Docker configuration
│   └── requirements.txt # Python dependencies
└── README.md
```

## Setup Instructions

### Option 1: Local Development

1. **Configure AWS Credentials**
   ```bash
   aws configure
   ```

2. **Initialize Terraform**
   ```bash
   terraform init
   ```

3. **Create a terraform.tfvars file**
   ```hcl
   aws_region = "us-west-2"
   key_name   = "your-key-pair-name"
   ```

4. **Deploy Infrastructure**
   ```bash
   terraform plan
   terraform apply
   ```

5. **Set up Python Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

6. **Configure MongoDB Connection**
   Create a `.env` file in the backend directory:
   ```
   MONGO_URI=mongodb://<EC2-PUBLIC-IP>:27017
   ```

7. **Run the Backend**
   ```bash
   uvicorn main:app --reload
   ```

### Option 2: Docker Deployment

1. **Build the Docker Image**
   ```bash
   cd backend
   docker build -t mongodb-api .
   ```

2. **Run the Container**
   ```bash
   docker run -d \
     --name mongodb-api \
     -p 8000:8000 \
     -e MONGO_URI=mongodb://<EC2-PUBLIC-IP>:27017 \
     mongodb-api
   ```

3. **Deploy to AWS ECR (Optional)**
   ```bash
   # Authenticate Docker to ECR
   aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws-account-id>.dkr.ecr.<region>.amazonaws.com

   # Create ECR repository
   aws ecr create-repository --repository-name mongodb-api

   # Tag the image
   docker tag mongodb-api:latest <aws-account-id>.dkr.ecr.<region>.amazonaws.com/mongodb-api:latest

   # Push the image
   docker push <aws-account-id>.dkr.ecr.<region>.amazonaws.com/mongodb-api:latest
   ```

## API Endpoints

- `GET /`: Health check
- `POST /items/`: Create a new item
- `GET /items/`: List all items
- `GET /items/{item_id}`: Get a specific item
- `DELETE /items/{item_id}`: Delete an item

## Infrastructure Details

- VPC with public subnet
- Security group allowing MongoDB (27017) and SSH (22) access
- EC2 instances running MongoDB
- Scalable configuration (adjust instance_count in variables.tf)

## Security Considerations

- The current setup allows access from any IP (0.0.0.0/0) to MongoDB port
- For production, restrict the CIDR blocks in the security group
- Consider using AWS Secrets Manager for sensitive data
- Enable MongoDB authentication
- When using Docker, ensure proper network security between containers
- Use AWS ECR private repositories for container images

## Cleanup

To destroy the infrastructure:
```bash
terraform destroy
```

To remove Docker containers and images:
```bash
docker stop mongodb-api
docker rm mongodb-api
docker rmi mongodb-api
```
