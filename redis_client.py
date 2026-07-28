# redis_client.py
import redis
from config import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,   # "redis" if calling from another container, "localhost" if local
    port=6379,
    db=0,
    decode_responses=True,
)