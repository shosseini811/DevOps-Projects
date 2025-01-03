# Kubernetes User Management Platform

A secure Flask-based web application for managing user authentication and Kubernetes namespace automation.

## Features

- User Authentication System
  - JWT-based authentication
  - Role-based access control (admin/user roles)
  - Secure password hashing
  - User activity tracking (last login, creation date)

- Admin Capabilities
  - User registration management
  - User listing and management
  - Role assignment

- Kubernetes Integration
  - Automatic namespace creation for users
  - Kubernetes configuration management
  - Support for both in-cluster and local development

- Database Integration
  - PostgreSQL backend
  - SQLAlchemy ORM
  - Automatic database initialization
  - User state persistence

## Prerequisites

- Python 3.10+
- PostgreSQL database
- Docker
- Kubernetes cluster (minikube, kind, or cloud provider)
- kubectl configured

## Local Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd KubernetesUserManagement
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
export DATABASE_URL="postgresql://postgres:123456@localhost:5432/k8s_users"
export JWT_SECRET_KEY="your-secret-key"  # Change in production
export ADMIN_PASSWORD="admin123"  # Change in production
```

5. Initialize the database:
```bash
python init_db.py
```

6. Run the application:
```bash
python app.py
```

The application will be available at http://localhost:5001

## Docker Deployment

1. Build the Docker image:
```bash
docker build -t k8s-user-management:latest .
```

2. Run the container:
```bash
docker run -p 5000:5000 \
  -e DATABASE_URL="postgresql://postgres:123456@host.docker.internal:5432/k8s_users" \
  -e JWT_SECRET_KEY="your-secret-key" \
  -e ADMIN_PASSWORD="admin123" \
  k8s-user-management:latest
```

## Kubernetes Deployment

1. Deploy PostgreSQL:
```bash
kubectl apply -f k8s/postgres.yaml
```

2. Create secrets:
```bash
kubectl apply -f k8s/secrets.yaml
```

3. Deploy the application:
```bash
kubectl apply -f k8s/deployment.yaml
```

## API Endpoints

### Authentication
- `POST /api/login` - User login
- `POST /api/register` - Register new user (admin only)

### Admin
- `GET /api/users` - List all users (admin only)

### Web Interface
- `GET /` - Home page

## Security Considerations

- Change all default passwords and secrets before deploying to production
- Use proper SSL/TLS in production
- Implement network policies in Kubernetes
- Regular security audits
- Monitor user activities and login attempts

## Testing

The project includes a comprehensive test suite:

```bash
python run_tests.py
```

## Dependencies

- Flask - Web framework
- Flask-SQLAlchemy - ORM for database operations
- Flask-JWT-Extended - JWT authentication
- psycopg2-binary - PostgreSQL adapter
- kubernetes - Kubernetes API client

- gunicorn - Production WSGI server

## License

MIT License 