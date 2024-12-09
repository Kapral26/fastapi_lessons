"""Пример описанного handler."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from dependencies import get_tasks_service, get_request_user_id
from exceptions import TaskNotFoundError
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
async def get_tasks(
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
) -> TaskSchema:
    task = await task_service.create_task(body, user_id)
    return task


@router.get("/name/{task_name}", response_model=TaskSchema)
async def get_task_by_name(
        task_name: str,
        task_service: Annotated[TaskService, Depends(get_tasks_service)],
) -> TaskSchema:
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
    try:
        task = await task_service.get_task_by_name(task_name)
    except TaskNotFoundError as error:
        raise HTTPException(HTTP_404_NOT_FOUND, detail=error.detail)
    return task


@router.get("/id/{task_id}", response_model=TaskSchema)
async def get_task_by_id(
        task_id: int,
        task_service: Annotated[TaskService, Depends(get_tasks_service)],
) -> TaskSchema:
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
    try:
        task = await task_service.get_task_by_id(task_id)
    except TaskNotFoundError as error:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=error.detail)
    return task


@router.get("/users-tasks", response_model=list[TaskSchema])
async def get_task_by_current_user(
        task_service: Annotated[TaskService, Depends(get_tasks_service)],
        user_id: int = Depends(get_request_user_id)
) -> list[TaskSchema]:
    try:
        tasks = await task_service.get_tasks_by_current_user(user_id)
    except TaskNotFoundError as error:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=error.detail)
    return tasks


@router.get("/users-tasks/{user_id}", response_model=list[TaskSchema])
async def get_user_tasks(
        task_service: Annotated[TaskService, Depends(get_tasks_service)],
        user_id: int
) -> list[TaskSchema]:
    try:
        task = await task_service.get_user_tasks(user_id)
    except TaskNotFoundError as error:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=error.detail)
    return task


@router.patch("/{task_id}", response_model=TaskSchema)
async def _update_task_name(
        task_id: int,
        new_name: str,
        task_service: Annotated[TaskService, Depends(get_tasks_service)],
        user_id: int = Depends(get_request_user_id),
) -> TaskSchema:
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
    try:
        updt_task = await task_service.update_task_name(task_id, new_name, user_id)
    except TaskNotFoundError as error:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=error.detail)
    return updt_task


@router.delete("/{task_id}", status_code=HTTP_204_NO_CONTENT)
async def _delete_task(
        task_id: int,
        task_service: Annotated[TaskService, Depends(get_tasks_service)],
        user_id: int = Depends(get_request_user_id),
) -> None:
    """
    Удаление задачи.

    Описание:
    - Удаляет задачу из базы данных.

    Аргументы:
    - task_id: Идентификатор задачи.
    """
    try:
        await task_service.delete_task(task_id)
    except TaskNotFoundError as error:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=error.detail)
