# post-service/config.py
import os

# gRPC server config
GRPC_HOST: str = os.getenv("POST_SERVICE_HOST", "0.0.0.0")
GRPC_PORT: int = int(os.getenv("POST_SERVICE_PORT", "50052"))

# Database config
POST_DB_URL: str = os.getenv(
    "POST_DB_URL",
    "postgresql://user:password@post-db:5432/postdb",
)

# Address of the user-service for gRPC calls
USER_SERVICE_ADDR: str = os.getenv(
    "USER_SERVICE_ADDR",
    "user-service:50051",
)
