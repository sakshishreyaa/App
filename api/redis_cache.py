import redis
import sys


async def redis_connection():
    try:
        client = redis.StrictRedis(
            host="localhost",
            port=6379,
            db=0,
            socket_timeout=5,
        )
        ping = client.ping()
        if ping is True:
            return client
    except Exception as e:
        print("AuthenticationError")
        sys.exit(1)
