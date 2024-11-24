"""Пример описанного handler."""

from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from dependencies import get_tasks_repository, get_tasks_service
from models import TaskModel
from repository import TaskRepository
from schemas.tasks import TaskDTO
from service.task_service import TaskService

# APIRouter - Дает возможность регистрировать роуты

router = APIRouter(
    # Префикс handler`а, чтобы ниже при регистрации к каждому не указывать
    prefix="/tasks",
    # Теги handler`а
    tags=["tasks"],
)


@router.get("/all", response_model=list[TaskDTO])
async def get_async_tasks(
    task_service: Annotated[TaskService, Depends(get_tasks_service)],
) -> list[TaskDTO] | None:
    """Get all tasks from the database.

    This endpoint returns a list of TaskDTO objects, which contains all the tasks in the database.
    The list will be empty if there are no tasks.

    The endpoint is designed to be used with the TaskService, which encapsulates the logic of getting all tasks from the database.
    """
    all_tasks = await task_service.get_tasks()
    return all_tasks


@router.post("/", status_code=HTTP_201_CREATED)
async def _create_task(
    task: TaskDTO,
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
) -> None:
    """Можно обратить внимание, что не указан как /create_task
    Так, как это POST запрос, оно является явным указанием.
    """
    await task_repository.create_task(task)


@router.get("/name/{task_name}", response_model=TaskDTO)
async def get_task_by_name(
    task_name: str,
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
) -> TaskModel | None:
    """Получение задачи по имени."""
    task = await task_repository.get_task_by_name(task_name)
    return task


@router.get("/id/{task_id}", response_model=TaskDTO)
async def get_task_by_id(
    task_id: int,
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
) -> TaskModel | None:
    """Получение задачи по имени."""
    task = await task_repository.get_task_by_id(task_id)
    return task


@router.patch("/{task_id}", response_model=TaskDTO)
async def _update_task(
    task_id: int,
    new_name: str,
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
) -> TaskModel | None:
    """Обновление имени задачи по id."""
    updt_task = await task_repository.update_task_name(task_id, new_name)
    return updt_task


@router.delete("/{task_id}", status_code=HTTP_204_NO_CONTENT)
async def _delete_task(
    task_id: int,
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)],
) -> None:
    """Удаление задачи по id."""
    await task_repository.delete_task(task_id)
