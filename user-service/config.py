# user-service/config.py
import os

# gRPC server config
GRPC_HOST: str = os.getenv("USER_SERVICE_HOST", "0.0.0.0")
GRPC_PORT: int = int(os.getenv("USER_SERVICE_PORT", "50051"))

# Database config
USER_DB_URL: str = os.getenv(
    "USER_DB_URL",
    "postgresql://user:password@user-db:5432/userdb",
)
