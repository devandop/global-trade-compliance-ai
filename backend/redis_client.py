import redis
import os

redis_url = os.getenv("REDIS_URL")
redis_client = redis.from_url(redis_url) 

def get_redis_client():
    return redis_client
