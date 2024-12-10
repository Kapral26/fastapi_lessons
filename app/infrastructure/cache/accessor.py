from redis import asyncio as redis

from app.settings.main_settings import Settings

settings = Settings()


def get_redis_connection() -> redis.Redis:
    """
    Функция для получения подключения к Redis.

    Описание:
    - Создает подключение к Redis с использованием настроек из файла settings.
    - Возвращает объект подключения к Redis.

    Возвращает:
    - Объект подключения к Redis.
    """
    redis_host = settings.redis_host
    redis_port = settings.redis_port
    redis_db = settings.redis_db
    return redis.Redis(host=redis_host, port=redis_port, db=redis_db)
