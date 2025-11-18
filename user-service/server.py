import time
import grpc
from concurrent import futures
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError  # 👈 new

from db import Base, engine, SessionLocal
from models import User
from config import GRPC_HOST, GRPC_PORT

import user_pb2
import user_pb2_grpc


def init_db_with_retry(retries: int = 10, delay: int = 2):
    """Wait for Postgres to be ready before creating tables."""
    for attempt in range(1, retries + 1):
        try:
            print(f"[user-service] Attempt {attempt}: initializing DB...")
            Base.metadata.create_all(bind=engine)
            print("[user-service] DB ready, tables created.")
            return
        except OperationalError as e:
            print(f"[user-service] DB not ready yet: {e}")
            if attempt == retries:
                print("[user-service] Giving up on DB connection.")
                raise
            time.sleep(delay)


# 🔥 call this BEFORE defining/starting the gRPC server
init_db_with_retry()


class UserServiceServicer(user_pb2_grpc.UserServiceServicer):
    def CreateUser(self, request, context):
        db: Session = SessionLocal()
        user = User(username=request.username, email=request.email)
        db.add(user)
        db.commit()
        db.refresh(user)
        db.close()

        return user_pb2.CreateUserResponse(
            user=user_pb2.User(
                id=user.id,
                username=user.username,
                email=user.email
            )
        )

    def GetUserById(self, request, context):
        db: Session = SessionLocal()
        user = db.query(User).filter(User.id == request.id).first()
        db.close()

        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return user_pb2.GetUserByIdResponse()

        return user_pb2.GetUserByIdResponse(
            user=user_pb2.User(
                id=user.id,
                username=user.username,
                email=user.email
            )
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(), server)
    server.add_insecure_port(f"{GRPC_HOST}:{GRPC_PORT}")
    print(f"[user-service] running at {GRPC_HOST}:{GRPC_PORT}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
