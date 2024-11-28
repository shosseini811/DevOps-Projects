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

## AWS Deployment

### Using CloudFormation

1. Navigate to the infrastructure directory:
   ```bash
   cd infrastructure
   ```

2. Deploy the CloudFormation stack:
   ```bash
   aws cloudformation create-stack \
     --stack-name openai-api-stack \
     --template-body file://cloudformation.yaml \
     --capabilities CAPABILITY_IAM
   ```

3. Monitor the stack creation:
   ```bash
   aws cloudformation describe-stacks --stack-name openai-api-stack
   ```

### Infrastructure Components

The CloudFormation template creates the following resources:

- VPC with public subnets across 2 availability zones
- Internet Gateway and route tables
- Application Load Balancer
- ECS Cluster running on Fargate
- ECS Task Definition and Service
- IAM roles and security groups
- Secrets Manager for OpenAI API key

### Environment Variables

The following environment variables are required:

- `OPENAI_API_KEY`: Your OpenAI API key (stored in AWS Secrets Manager)
- `PORT`: Container port (default: 5000)

### Troubleshooting

1. **Task Failures**
   - Check ECS task logs in CloudWatch
   - Verify IAM roles have correct permissions
   - Ensure Secrets Manager access is configured

2. **Network Issues**
   - Verify security group rules
   - Check VPC and subnet configurations
   - Confirm load balancer health checks

3. **Common Errors**
   - `ResourceInitializationError`: Check ECS task execution role permissions
   - `SecretNotFound`: Verify secret ARN and permissions
   - `ContainerPortConflict`: Ensure port mappings are correct

### Monitoring

1. **CloudWatch Logs**
   - ECS task logs are available in CloudWatch under `/ecs/{environment}-openai-api`
   - Application logs show API requests and errors

2. **Metrics**
   - ECS Service metrics (CPU, Memory)
   - ALB metrics (Request count, latency)
   - Target group health

### Cleanup

To remove all AWS resources:

```bash
aws cloudformation delete-stack --stack-name openai-api-stack
```

## Security Considerations

1. **API Key Management**
   - OpenAI API key is stored in AWS Secrets Manager
   - Access is restricted through IAM roles
   - No hardcoded secrets in code or configuration

2. **Network Security**
   - VPC with private subnets (if needed)
   - Security groups restrict access
   - ALB terminates SSL/TLS

3. **IAM Best Practices**
   - Least privilege principle
   - Task execution role with minimal permissions
   - Regular rotation of credentials

## Testing the API

After deployment, you can test the API using various methods:

### Using cURL

1. Test the health endpoint:
```bash
curl -X GET "http://<your-load-balancer-dns>/health"
```

2. Test the chat endpoint:
```bash
curl -X POST "http://<your-load-balancer-dns>/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the capital of France?"}'
```

### Using Python

```python
import requests

# Base URL - replace with your Load Balancer DNS
BASE_URL = "http://<your-load-balancer-dns>"

# Test health endpoint
response = requests.get(f"{BASE_URL}/health")
print("Health check:", response.json())

# Test chat endpoint
response = requests.post(
    f"{BASE_URL}/api/chat",
    json={"message": "What is the capital of France?"}
)
print("Chat response:", response.json())
```

### Using Postman

1. Health Check Endpoint:
   - Method: GET
   - URL: `http://<your-load-balancer-dns>/health`
   - Expected Response: `{"status": "healthy"}`

2. Chat Endpoint:
   - Method: POST
   - URL: `http://<your-load-balancer-dns>/api/chat`
   - Headers: 
     - Content-Type: application/json
   - Body (raw JSON):
     ```json
     {
         "message": "What is the capital of France?"
     }
     ```

### Example Responses

1. Health Check Response:
```json
{
    "status": "healthy"
}
```

2. Chat Response:
```json
{
    "response": "The capital of France is Paris. It is known as the 'City of Light' and is famous for its art, culture, fashion, and landmarks like the Eiffel Tower."
}
```

### Error Handling

The API returns appropriate HTTP status codes:

- 200: Successful request
- 400: Bad request (e.g., missing message)
- 500: Server error (e.g., OpenAI API issues)

Example error response:
```json
{
    "error": "Message is required"
}
```

### Load Testing

For load testing, you can use tools like Apache Bench or Artillery:

```bash
# Using Apache Bench (100 requests, 10 concurrent)
ab -n 100 -c 10 -T 'application/json' -p payload.json http://<your-load-balancer-dns>/api/chat
```

Where payload.json contains:
```json
{
    "message": "Hello, how are you?"
}
```

## Performance Considerations

1. **Scaling**
   - The ECS service automatically scales based on CPU/Memory usage
   - Default configuration: 2 tasks minimum
   - Adjust task count in CloudFormation template if needed

2. **Monitoring**
   - Monitor API latency through CloudWatch metrics
   - Set up CloudWatch alarms for error rates
   - Track ECS service metrics for scaling decisions

3. **Cost Optimization**
   - Use Fargate Spot for non-production workloads
   - Monitor API usage to optimize instance sizes
   - Set up AWS Budget alerts

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Security Notes

- Always keep your OpenAI API key secure
- Use AWS Secrets Manager for production deployments
- Implement proper authentication for the API endpoints
- Use HTTPS in production
