#!/bin/bash

# Exit on error
set -e

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "AWS CLI is not installed. Please install it first."
    exit 1
fi

# Check if required environment variables are set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "OPENAI_API_KEY is not set. Please set it."
    exit 1
fi

# Get AWS Account ID dynamically
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION="us-east-1"

# Create ECR repository if it doesn't exist
aws ecr describe-repositories --repository-names openai-api-app || \
    aws ecr create-repository --repository-name openai-api-app

# Authenticate Docker with ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Build and push Docker image
docker build -t openai-api-app .
docker tag openai-api-app:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/openai-api-app:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/openai-api-app:latest

# Deploy CloudFormation stack
aws cloudformation deploy \
    --template-file infrastructure/cloudformation.yaml \
    --stack-name openai-api-stack \
    --parameter-overrides \
        EnvironmentName=dev \
        OpenAIApiKey=$OPENAI_API_KEY \
        ContainerPort=5000 \
    --capabilities CAPABILITY_IAM

# Get the Load Balancer DNS name
echo "Deployment completed! Getting Load Balancer DNS..."
LB_DNS=$(aws cloudformation describe-stacks \
    --stack-name openai-api-stack \
    --query 'Stacks[0].Outputs[?OutputKey==`LoadBalancerDNS`].OutputValue' \
    --output text)

echo "Your application is deployed!"
echo "Load Balancer DNS: $LB_DNS"
echo "You can access your API at: http://$LB_DNS"
