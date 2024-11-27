"""Пример описанного handler."""

from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.status import HTTP_204_NO_CONTENT

from dependencies import get_tasks_repository, get_tasks_service, get_request_user_id
from models import TaskModel
from repository import TaskRepository
from schemas.tasks import TaskSchema, TaskCreateSchema
from service.task_service import TaskService

# APIRouter - Дает возможность регистрировать роуты

router = APIRouter(
    # Префикс handler`а, чтобы ниже при регистрации к каждому не указывать
    prefix="/tasks",
    # Теги handler`а
    tags=["tasks"],
)


@router.get("/all", response_model=list[TaskSchema])
async def get_async_tasks(
    task_service: Annotated[TaskService, Depends(get_tasks_service)],
) -> list[TaskSchema] | None:
    """
    Получение всех задач.

    Описание:
    - Выполняет запрос на выборку всех задач из базы данных.
    - Возвращает список моделей TaskModel.

    Возвращает:
    - Список моделей TaskModel.
    """
    all_tasks = await task_service.get_tasks()
    return all_tasks


@router.post("/", response_model=TaskSchema)
async def create_task(
    body: TaskCreateSchema,
    task_service: Annotated[TaskService, Depends(get_tasks_service)],
    user_id: int = Depends(get_request_user_id),
):
    task = await task_service.create_task(body, user_id)
    return task


@router.get("/name/{task_name}", response_model=TaskSchema)
async def get_task_by_name(
    task_name: str,
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
) -> TaskModel | None:
    """
    Получение задачи по имени.

    Описание:
    - Выполняет запрос на выборку задачи по имени.
    - Возвращает первую найденную задачу или None, если задача не найдена.

    Аргументы:
    - task_name: Имя задачи.

    Возвращает:
    - Модель TaskModel, если задача найдена.
    - None, если задача не найдена.
    """
    task = await task_repository.get_task_by_name(task_name)
    return task


@router.get("/id/{task_id}", response_model=TaskSchema)
async def get_task_by_id(
    task_id: int,
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
) -> TaskModel | None:
    """
    Получение задачи по идентификатору.

    Описание:
    - Выполняет запрос на выборку задачи по идентификатору.
    - Возвращает первую найденную задачу или None, если задача не найдена.

    Аргументы:
    - task_id: Идентификатор задачи.

    Возвращает:
    - Модель TaskModel, если задача найдена.
    - None, если задача не найдена.
    """
    task = await task_repository.get_task_by_id(task_id)
    return task


@router.patch("/{task_id}", response_model=TaskSchema)
async def _update_task(
    task_id: int,
    new_name: str,
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
) -> TaskModel | None:
    """
    Обновление имени задачи.

    Описание:
    - Обновляет имя задачи в базе данных.
    - Возвращает обновленную задачу.

    Аргументы:
    - task_id: Идентификатор задачи.
    - new_name: Новое имя задачи.

    Возвращает:
    - Обновленную задачу в формате TaskModel, если задача найдена.
    - None, если задача не найдена.
    """
    updt_task = await task_repository.update_task_name(task_id, new_name)
    return updt_task


@router.delete("/{task_id}", status_code=HTTP_204_NO_CONTENT)
async def _delete_task(
    task_id: int,
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
) -> None:
    """
    Удаление задачи.

    Описание:
    - Удаляет задачу из базы данных.

    Аргументы:
    - task_id: Идентификатор задачи.
    """
    await task_repository.delete_task(task_id)
