# MiniSocial – gRPC Microservices Demo

MiniSocial is a lightweight, production-style microservices architecture showcasing:

- **gRPC communication** between services  
- **FastAPI API Gateway**  
- **PostgreSQL per-service databases**  
- **Docker Compose orchestration**  
- **Clean service separation** following real microservice principles  

This project demonstrates how modern backend systems structure independent services that communicate efficiently using gRPC.

---

## 🏗 Architecture Overview

```mermaid
graph LR
    client[Client / curl / Frontend] --> gateway[API Gateway (FastAPI)]
    gateway -->|gRPC| usersvc[User Service]
    gateway -->|gRPC| postsvc[Post Service]
    usersvc -->|SQL| userdb[(user-db)]
    postsvc -->|SQL| postdb[(post-db)]
    postsvc -->|gRPC validate user| usersvc
```

---

## 📦 Services

### **1. API Gateway (FastAPI)**
- Exposes HTTP endpoints  
- Translates HTTP → gRPC  
- Aggregates data from user-service and post-service  

### **2. User Service (Python gRPC)**
- Creates and fetches users  
- Owns its own Postgres DB  
- Exposes `CreateUser` and `GetUserById` RPCs  

### **3. Post Service (Python gRPC)**
- Creates posts and lists posts by user  
- Calls **user-service via gRPC** internally to validate `user_id`  
- Owns its own Postgres DB  

---

## 🧪 Endpoints (from API Gateway)

### Create User
```
POST /users?username=<name>&email=<email>
```

### Create Post
```
POST /posts?user_id=<id>&content=<string>
```

### Get Posts With User Info
```
GET /users/<id>/posts
```

---

## 🐳 Running the Project

From the `deploy/` directory:

```bash
docker compose up --build
```

Services:
- API Gateway → `localhost:8000`
- User Service → internal gRPC `user-service:50051`
- Post Service → internal gRPC `post-service:50052`

---

## 💾 Testing (Git Bash)

### Create user:
```bash
curl -X POST "http://localhost:8000/users?username=varun&email=varun@example.com"
```

### Create post:
```bash
curl -X POST "http://localhost:8000/posts?user_id=1&content=Hello%20from%20Minisocial"
```

### Get posts:
```bash
curl "http://localhost:8000/users/1/posts"
```

---

## 🗂 Folder Structure

```
MiniSocial/
│
├── proto/                 # gRPC proto files
│
├── user-service/          # User microservice
│   ├── server.py
│   ├── models.py
│   ├── db.py
│   ├── config.py
│   ├── user_pb2.py
│   └── user_pb2_grpc.py
│
├── post-service/          # Post microservice
│   ├── server.py
│   ├── models.py
│   ├── db.py
│   ├── config.py
│   ├── post_pb2.py
│   ├── post_pb2_grpc.py
│   ├── user_pb2.py
│   └── user_pb2_grpc.py
│
├── api-gateway/           # HTTP → gRPC gateway
│   ├── main.py
│   ├── config.py
│   ├── user_pb2.py
│   ├── user_pb2_grpc.py
│   ├── post_pb2.py
│   └── post_pb2_grpc.py
│
└── deploy/
    └── docker-compose.yml
```

---

## 🎯 Why This Project Is Valuable

- Demonstrates **true microservice boundaries**
- Shows **gRPC usage**, for backend roles
- Includes **service-to-service communication**
- Uses **Docker Compose** for reproducible deployment
- Mimics real production patterns (per-service DB, gateway, retry logic)

---

## 👤 Author
Varun Date  
**MiniSocial – Microservices Architecture Demo**
