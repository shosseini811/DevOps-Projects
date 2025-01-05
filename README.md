# FastAPI Monitoring and Logging Demo

This project demonstrates a production-ready FastAPI setup with monitoring and logging capabilities.

## Features

- FastAPI backend with structured logging
- Prometheus metrics integration
- Grafana dashboards for visualization
- Docker and Docker Compose setup
- Built-in health checks and monitoring endpoints

## Prerequisites

- Docker and Docker Compose
- Python 3.9+ (for local development)

## Quick Start

1. Clone the repository
2. Run the stack:
   ```bash
   docker-compose up --build
   ```

## Accessing Services

- FastAPI Application: http://localhost:8000
- FastAPI Swagger Docs: http://localhost:8000/docs
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

## Monitoring Endpoints

- Application Health: http://localhost:8000/health
- Metrics: http://localhost:8000/metrics

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

3. Run the application:
   ```bash
   python src/main.py
   ```

## Logging

The application uses structured logging with the following features:
- Request/response logging with timing
- JSON format for easy parsing
- Correlation IDs for request tracking

## Metrics

The following metrics are available:
- Request latency
- Request counts by endpoint
- HTTP status codes
- System metrics (CPU, memory)
