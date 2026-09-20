from fastapi import APIRouter
from app.core.redis_client import redis_client

router = APIRouter(
    prefix="/redis",
    tags=["Redis"]
)


@router.get("/test")
def test_redis():
    redis_client.set("test_key", "Redis is working")

    value = redis_client.get("test_key")

    return {
        "message": value
    }