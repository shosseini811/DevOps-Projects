# OpenAI API AWS Deployment

This project demonstrates a simple Flask application that integrates with OpenAI's API and can be deployed on AWS using Docker containers.

## Prerequisites

- Python 3.9+
- Docker
- AWS Account
- OpenAI API Key

## Local Setup

1. Clone the repository
2. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
3. Add your OpenAI API key to the `.env` file

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:
   ```bash
   python app.py
   ```

## Docker Build & Run

Build the Docker image:
```bash
docker build -t openai-api-app .
```

Run the container:
```bash
docker run -p 5000:5000 --env-file .env openai-api-app
```

## API Endpoints

1. Health Check:
   ```
   GET /health
   ```

2. Chat Completion:
   ```
   POST /api/chat
   Content-Type: application/json

   {
       "message": "Your message here"
   }
   ```

## AWS Deployment Steps

1. Create an ECR repository:
   ```bash
   aws ecr create-repository --repository-name openai-api-app
   ```

2. Authenticate Docker with ECR:
   ```bash
   aws ecr get-login-password --region your-region | docker login --username AWS --password-stdin your-account-id.dkr.ecr.your-region.amazonaws.com
   ```

3. Tag and push the image:
   ```bash
   docker tag openai-api-app:latest your-account-id.dkr.ecr.your-region.amazonaws.com/openai-api-app:latest
   docker push your-account-id.dkr.ecr.your-region.amazonaws.com/openai-api-app:latest
   ```

4. Deploy using AWS ECS or EKS (detailed instructions to be added based on preference)

## Security Notes

- Always keep your OpenAI API key secure
- Use AWS Secrets Manager for production deployments
- Implement proper authentication for the API endpoints
- Use HTTPS in production
