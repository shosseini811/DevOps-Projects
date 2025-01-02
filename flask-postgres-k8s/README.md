# Flask PostgreSQL Kubernetes Todo App

A modern Todo application built with Flask and PostgreSQL, containerized with Docker and orchestrated using Kubernetes.

## 🚀 Features

- RESTful API for Todo management
- PostgreSQL database for persistent storage
- Docker containerization
- Kubernetes deployment configuration
- Simple web interface

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **Frontend**: HTML/JavaScript

## 📋 Prerequisites

- Docker
- Kubernetes cluster (Minikube or any other Kubernetes cluster)
- kubectl CLI
- Python 3.9+ (for local development)

## 🔧 Environment Variables

The application requires the following environment variables:

```env
POSTGRES_USER=<database_user>
POSTGRES_PASSWORD=<database_password>
POSTGRES_HOST=<database_host>
POSTGRES_PORT=<database_port>
POSTGRES_DB=<database_name>
```

## 🚀 Getting Started

### Local Development

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables
5. Run the application:
   ```bash
   python app.py
   ```

### Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t flask-todo-app .
   ```
2. Run the container:
   ```bash
   docker run -p 5001:5001 --env-file .env flask-todo-app
   ```

### Kubernetes Deployment

1. Apply the Kubernetes configurations:
   ```bash
   kubectl apply -f k8s/postgres.yaml
   kubectl apply -f k8s/flask-app.yaml
   ```
2. Wait for the pods to be ready:
   ```bash
   kubectl get pods
   ```

## 🔄 API Endpoints

- `GET /todos` - Retrieve all todos
- `POST /todos` - Create a new todo
- `PUT /todos/<id>` - Update a todo
- `DELETE /todos/<id>` - Delete a todo

## 📁 Project Structure

```
flask-postgres-k8s/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── k8s/               # Kubernetes manifests
│   ├── flask-app.yaml
│   └── postgres.yaml
└── templates/         # HTML templates
    └── index.html
```

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📝 License

This project is open source and available under the [MIT License](LICENSE). 