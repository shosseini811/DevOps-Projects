import structlog
from fastapi import FastAPI, Request
from prometheus_fastapi_instrumentator import Instrumentator
import time

# Configure structured logging
logger = structlog.get_logger()

app = FastAPI(title="FastAPI Monitoring Demo")

# Initialize Prometheus metrics
Instrumentator().instrument(app).expose(app)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(
        "request_processed",
        path=request.url.path,
        method=request.method,
        processing_time=process_time,
    )
    return response

@app.get("/")
async def root():
    logger.info("root_endpoint_called")
    return {"message": "Hello World"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 