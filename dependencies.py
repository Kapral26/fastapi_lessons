from typing import Annotated

from fastapi import Depends

from cache import get_redis_connection
from database import async_session_factory
from repository import TaskRepository, TaskCacheRepository
from service import TaskService


def get_tasks_repository() -> TaskRepository:
    """
    Create a :class:`TaskRepository` from the default async session factory.

    :return: a :class:`TaskRepository` instance.
    """
    return TaskRepository(async_session_factory)


def get_task_cache_repository() -> TaskCacheRepository:
    """
    Create a :class:`CacheTaskRepository` from the default Redis connection.

    :return: a :class:`CacheTaskRepository` instance.
    """
    return TaskCacheRepository(get_redis_connection())


def get_tasks_service(
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
    task_cache_repository: Annotated[TaskCacheRepository, Depends(get_task_cache_repository)],
) -> TaskService:
    """
    Create a :class:`TaskService` from the default :class:`TaskRepository` and :class:`CacheTaskRepository`.

    :param task_repository: a :class:`TaskRepository` instance.
    :param task_cache_repository: a :class:`CacheTaskRepository` instance.
    :return: a :class:`TaskService` instance.
    """
    return TaskService(task_repository=task_repository, task_cache_repository=task_cache_repository)
