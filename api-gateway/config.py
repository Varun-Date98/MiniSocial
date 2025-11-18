# api-gateway/config.py
import os

# FastAPI / Uvicorn config
API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
API_PORT: int = int(os.getenv("API_PORT", "8000"))

# Downstream gRPC services
USER_SERVICE_ADDR: str = os.getenv(
    "USER_SERVICE_ADDR",
    "user-service:50051",
)

POST_SERVICE_ADDR: str = os.getenv(
    "POST_SERVICE_ADDR",
    "post-service:50052",
)
