import redis
import os

def get_redis_client():
    return redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=0)
