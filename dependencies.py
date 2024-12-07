from typing import Annotated

from fastapi import Depends, security, Security, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from cache import get_redis_connection
from database import async_session_factory
from exceptions import TokenIsNotCorrectError, TokenExpiredError
from repository import TaskRepository, TaskCacheRepository, UserRepository
from service import TaskService
from service.auth_service import AuthService
from service.user_service import UserService
from settings import Settings


async def get_tasks_repository() -> TaskRepository:
    """
    Функция для получения экземпляра класса TaskRepository.

    :return: TaskRepository: Экземпляр класса TaskRepository,
     который используется для работы с задачами в базе данных.

    Примечание:
    Эта функция используется для получения экземпляра класса TaskRepository,
     который используется для работы с задачами в базе данных.
    Экземпляр класса TaskRepository создается с использованием фабрики асинхронных сессий async_session_factory.
    """
    return TaskRepository(async_session_factory)


async def get_task_cache_repository() -> TaskCacheRepository:
    """
    Функция для получения экземпляра класса TaskCacheRepository.

    :return: TaskCacheRepository: Экземпляр класса TaskCacheRepository,
     который используется для работы с кэшем задач в Redis.

    Примечание:
    Эта функция используется для получения экземпляра класса TaskCacheRepository,
     который используется для работы с кэшем задач в Redis.
    Экземпляр класса TaskCacheRepository создается с использованием функции get_redis_connection(),
     которая возвращает соединение с Redis.
    """
    return TaskCacheRepository(get_redis_connection())


async def get_tasks_service(
        task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
        task_cache_repository: Annotated[
            TaskCacheRepository, Depends(get_task_cache_repository)
        ],
) -> TaskService:
    """
    Функция для получения экземпляра класса TaskService.

    Параметры:
    task_repository (Annotated[TaskRepository, Depends(get_tasks_repository)]): Экземпляр класса TaskRepository,
     который используется для работы с задачами в базе данных.
    task_cache_repository (Annotated[TaskCacheRepository, Depends(get_task_cache_repository)]):
    Экземпляр класса TaskCacheRepository, который используется для работы с кэшем задач в Redis.

    Возвращает:
    TaskService: Экземпляр класса TaskService, который используется для работы с задачами.

    Примечание:
    Эта функция используется для получения экземпляра класса TaskService, который используется для работы с задачами.
    Экземпляры классов TaskRepository и TaskCacheRepository передаются в качестве параметров функции
     и используются для создания экземпляра класса TaskService.
    """
    return TaskService(
            task_repository=task_repository, task_cache_repository=task_cache_repository
    )


async def get_user_repository() -> UserRepository:
    """
    Функция для получения экземпляра класса UserRepository.

    Возвращает:
    UserRepository: Экземпляр класса UserRepository, который используется для работы с пользователями в базе данных.

    Примечание:
    Эта функция используется для получения экземпляра класса UserRepository,
    который используется для работы с пользователями в базе данных.
    Экземпляр класса UserRepository создается с использованием фабрики асинхронных сессий async_session_factory.
    """
    return UserRepository(session_factory=async_session_factory)


async def get_auth_service(
        user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> AuthService:
    """
    Функция для получения экземпляра класса AuthService.

    Параметры:
    user_repository (Annotated[UserRepository, Depends(get_user_repository)]): Экземпляр класса UserRepository,
    который используется для работы с пользователями в базе данных.

    Возвращает:
    AuthService: Экземпляр класса AuthService, который используется для работы с аутентификацией пользователей.

    Примечание:
    Эта функция используется для получения экземпляра класса AuthService,
    который используется для работы с аутентификацией пользователей.
    Экземпляр класса UserRepository передается в качестве параметра функции и
     используется для создания экземпляра класса AuthService.
    """
    return AuthService(user_repository=user_repository, settings=Settings())


async def get_user_service(
        user_repository: Annotated[UserRepository, Depends(get_user_repository)],
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserService:
    """
    Функция для получения экземпляра класса UserService.

    Параметры:
    user_repository (Annotated[UserRepository, Depends(get_user_repository)]): Экземпляр класса UserRepository,
    который используется для работы с пользователями в базе данных.
    auth_service (Annotated[AuthService, Depends(get_auth_service)]): Экземпляр класса AuthService,
    который используется для работы с аутентификацией пользователей.

    Возвращает:
    UserService: Экземпляр класса UserService, который используется для работы с пользователями.

    Примечание:
    Эта функция используется для получения экземпляра класса UserService,
    который используется для работы с пользователями. Экземпляры классов UserRepository и AuthService
    передаются в качестве параметров функции и используются для создания экземпляра класса UserService.
    """
    return UserService(user_repository=user_repository, auth_service=auth_service)


reusable_oauth2 = security.HTTPBearer()


async def get_request_user_id(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2),  # noqa: B008
) -> int:
    try:
        user_id = await auth_service.get_user_id_from_access_token(token.credentials)
    except TokenIsNotCorrectError as error:
        # Обычно HTTPException вызывается на уровне handlers,
        # но т.к. данный метод по Depends вызывается только там, в таком случае допускается.
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=error.detail)
    except TokenExpiredError as error:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail=error.detail)
    return user_id
