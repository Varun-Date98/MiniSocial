import time
import grpc
from concurrent import futures
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError  # 👈 new

from db import Base, engine, SessionLocal
from models import Post
from config import GRPC_HOST, GRPC_PORT, USER_SERVICE_ADDR

import post_pb2
import post_pb2_grpc
import user_pb2
import user_pb2_grpc


def init_db_with_retry(retries: int = 10, delay: int = 2):
    for attempt in range(1, retries + 1):
        try:
            print(f"[post-service] Attempt {attempt}: initializing DB...")
            Base.metadata.create_all(bind=engine)
            print("[post-service] DB ready, tables created.")
            return
        except OperationalError as e:
            print(f"[post-service] DB not ready yet: {e}")
            if attempt == retries:
                print("[post-service] Giving up on DB connection.")
                raise
            time.sleep(delay)


init_db_with_retry()


def get_user_stub():
    channel = grpc.insecure_channel(USER_SERVICE_ADDR)
    return user_pb2_grpc.UserServiceStub(channel)


class PostServiceServicer(post_pb2_grpc.PostServiceServicer):
    def __init__(self):
        self.user_stub = get_user_stub()

    def CreatePost(self, request, context):
        # Validate user via user-service
        try:
            _ = self.user_stub.GetUserById(
                user_pb2.GetUserByIdRequest(id=request.user_id)
            )
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("User does not exist")
                return post_pb2.CreatePostResponse()
            raise

        db: Session = SessionLocal()
        post = Post(user_id=request.user_id, content=request.content)
        db.add(post)
        db.commit()
        db.refresh(post)
        db.close()

        return post_pb2.CreatePostResponse(
            post=post_pb2.Post(
                id=post.id,
                user_id=post.user_id,
                content=post.content,
                created_at=str(post.created_at),
            )
        )

    def ListPostsByUser(self, request, context):
        db: Session = SessionLocal()
        posts = db.query(Post).filter(Post.user_id == request.user_id).all()
        db.close()

        return post_pb2.ListPostsByUserResponse(
            posts=[
                post_pb2.Post(
                    id=p.id,
                    user_id=p.user_id,
                    content=p.content,
                    created_at=str(p.created_at),
                )
                for p in posts
            ]
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    post_pb2_grpc.add_PostServiceServicer_to_server(PostServiceServicer(), server)
    server.add_insecure_port(f"{GRPC_HOST}:{GRPC_PORT}")
    print(f"[post-service] running at {GRPC_HOST}:{GRPC_PORT}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
