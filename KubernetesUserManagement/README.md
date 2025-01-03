# Kubernetes User Management Platform

A secure, scalable platform for managing Kubernetes user access and resource quotas.

## Features

- User authentication with JWT
- Resource quota management
- Kubernetes namespace automation
- PostgreSQL database integration
- Containerized deployment
- Kubernetes-native deployment

## Prerequisites

- Docker
- Kubernetes cluster (minikube, kind, or cloud provider)
- kubectl configured
- Python 3.10+

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd KubernetesUserManagement
```

2. Build the Docker image:
```bash
docker build -t k8s-user-management:latest .
```

3. Create Kubernetes secrets (modify values for production):
```bash
kubectl apply -f k8s/secrets.yaml
```

4. Deploy PostgreSQL:
```bash
kubectl apply -f k8s/postgres.yaml
```

5. Deploy the application:
```bash
kubectl apply -f k8s/deployment.yaml
```

## API Endpoints

### Authentication
- POST /api/register - Register a new user
- POST /api/login - Login and get JWT token

### Resource Management
- POST /api/request-resources - Request resource quota
- GET /api/resources - Get user's resource quotas

## Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run locally:
```bash
python files.py
```

## Security Notes

- Change all default secrets in `secrets.yaml` before deploying to production
- Use proper SSL/TLS in production
- Implement proper role-based access control (RBAC)
- Regular security audits and updates

## Monitoring

The application can be monitored using:
- Kubernetes dashboard
- Prometheus metrics (endpoint: /metrics)
- Grafana dashboards (setup separately)

## License

MIT License 