# user-service/Dockerfile
FROM python:3.11-slim

# System deps for psycopg2/Postgres
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code (including *_pb2.py files)
COPY . .

EXPOSE 50051

CMD ["python", "server.py"]
