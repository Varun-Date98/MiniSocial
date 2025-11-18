from fastapi import FastAPI, HTTPException
import grpc

import user_pb2
import user_pb2_grpc
import post_pb2
import post_pb2_grpc

from config import USER_SERVICE_ADDR, POST_SERVICE_ADDR


app = FastAPI(title="MiniSocial API Gateway")


def get_user_stub():
    channel = grpc.insecure_channel(USER_SERVICE_ADDR)
    return user_pb2_grpc.UserServiceStub(channel)


def get_post_stub():
    channel = grpc.insecure_channel(POST_SERVICE_ADDR)
    return post_pb2_grpc.PostServiceStub(channel)


@app.post("/users")
def create_user(username: str, email: str):
    stub = get_user_stub()
    resp = stub.CreateUser(user_pb2.CreateUserRequest(username=username, email=email))
    return {"id": resp.user.id, "username": resp.user.username, "email": resp.user.email}


@app.post("/posts")
def create_post(user_id: int, content: str):
    post_stub = get_post_stub()
    try:
        resp = post_stub.CreatePost(post_pb2.CreatePostRequest(user_id=user_id, content=content))
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
            raise HTTPException(status_code=400, detail=e.details())
        raise
    return {
        "id": resp.post.id,
        "user_id": resp.post.user_id,
        "content": resp.post.content,
        "created_at": resp.post.created_at,
    }


@app.get("/users/{user_id}/posts")
def get_posts_for_user(user_id: int):
    user_stub = get_user_stub()
    post_stub = get_post_stub()

    # ensure user exists
    try:
        user_resp = user_stub.GetUserById(user_pb2.GetUserByIdRequest(id=user_id))
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(status_code=404, detail="User not found")
        raise

    posts_resp = post_stub.ListPostsByUser(post_pb2.ListPostsByUserRequest(user_id=user_id))
    return {
        "user": {
            "id": user_resp.user.id,
            "username": user_resp.user.username,
            "email": user_resp.user.email,
        },
        "posts": [
            {
                "id": p.id,
                "content": p.content,
                "created_at": p.created_at,
            }
            for p in posts_resp.posts
        ],
    }
