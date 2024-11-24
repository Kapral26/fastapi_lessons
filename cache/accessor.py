import asyncio

import redis

import redis.asyncio

from settings import Settings

settings = Settings()


def get_redis_connection() -> redis.Redis:
    """Синхронное подключение к Redis."""
    redis_host = settings.redis_host
    redis_port = settings.redis_port
    redis_db = settings.redis_db
    return redis.Redis(host=redis_host, port=redis_port, db=redis_db)


# FIXME добавить асинхронность
# async def get_redis_connection_async() -> redis.asyncio.client.Redis:
#     """АСинхронное подключение к Redis."""
#     redis_host = settings.redis_host
#     redis_port = settings.redis_port
#     redis_db = settings.redis_db
#     return redis.asyncio.Redis(host=redis_host, port=redis_port, db=redis_db)
