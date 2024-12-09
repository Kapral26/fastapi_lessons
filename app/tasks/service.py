from dataclasses import dataclass

from app.exceptions import TaskNotFoundError
from app.tasks import TaskCacheRepository, TaskRepository, TaskSchema, TaskCreateSchema


@dataclass
class TaskService:
    """
    Класс для работы с задачами.

    Атрибуты:
    task_repository (TaskRepository): Экземпляр класса TaskRepository,
     который используется для работы с задачами в базе данных.
    task_cache_repository (TaskCacheRepository): Экземпляр класса TaskCacheRepository,
     который используется для работы с кэшем задач в Redis.

    Методы:
    get_tasks(self) -> list[TaskSchema] | None: Получает список задач.
    """

    task_repository: TaskRepository
    task_cache_repository: TaskCacheRepository

    async def get_tasks(
            self
    ) -> list[TaskSchema] | None:
        """
        Получает список задач.

        Описание:
        - Пытается получить список задач из кэша.
        - Если список задач не найден в кэше, получает список задач из базы данных.
        - Сохраняет список задач в кэш.

        Возвращает:
        - Список задач в формате TaskSchema, если задачи найдены.
        - None, если список задач пуст или ключ отсутствует.
        """
        if all_tasks := await self.task_cache_repository.get_tasks():
            pass
        else:
            all_tasks = await self.task_repository.get_tasks()
            tasks_schema = [TaskSchema.model_validate(task) for task in all_tasks]
            await self.task_cache_repository.set_tasks(tasks_schema)

        return all_tasks

    async def create_task(
            self,
            body: TaskCreateSchema,
            user_id: int
    ) -> TaskSchema:
        """
        Создает задачу и предоставляет о ней информацию.
        :param body: Объект TaskCreateSchema
        :param user_id: Идентификатор пользователя.
        :return: Информация о задаче.
        """
        task_id = await self.task_repository.create_task(body, user_id)
        task = await self.task_repository.get_task_by_id(task_id)
        return TaskSchema.model_validate(task)

    async def update_task_name(
            self,
            task_id: int,
            name: str,
            user_id: int
    ) -> TaskSchema:
        """
        Обновляет имя задачи.
        :param task_id: Идентификатор задачи
        :param name: Новое имя задачи.
        :param user_id: Идентификатор пользователя.
        :raise TaskNotFoundError: Если задачи для обновления не существует.
        :return: Обновленная задача.
        """
        updated_task = await self.task_repository.update_task_name(task_id, name, user_id)
        if not updated_task:
            raise TaskNotFoundError
        return TaskSchema.model_validate(updated_task)

    async def delete_task(
            self,
            task_id: int,
    ) -> None:
        """
        Удаляет задачу.
        :param task_id: Идентификатор задачи
        :raise TaskNotFoundError: Если задачи для обновления не существует.
        """
        updated_task = await self.task_repository.delete_task(task_id)
        await self.task_cache_repository.delete_task(task_id)
        if not updated_task:
            raise TaskNotFoundError

    async def get_task_by_id(
            self,
            task_id: int
    ) -> TaskSchema:
        """
        Возвращает информацию о задаче на основании идентификатора.
        :param task_id: Идентификатор задачи
        :raise TaskNotFoundError: Если задачи для обновления не существует.
        """
        task = await self.task_repository.get_task_by_id(task_id)
        if not task:
            raise TaskNotFoundError
        return TaskSchema.model_validate(task)

    async def get_task_by_name(
            self,
            name: str
    ) -> TaskSchema:
        """
        Возвращает информацию о задаче на основании названия.
        :param name: Название задачи
        :raise TaskNotFoundError: Если задачи для обновления не существует.
        """
        task = await self.task_repository.get_task_by_name(name)
        if not task:
            raise TaskNotFoundError
        return TaskSchema.model_validate(task)

    async def get_tasks_by_current_user(
            self,
            user_id: int,
    ) -> list[TaskSchema]:
        """
        Возвращает список задач, созданных авторизованным пользователем.
        :param user_id: Идентификатор авторизованного пользователя.
        :raise TaskNotFoundError: Если задачи для обновления не существует.
        :return: Задачи пользователя.
        """
        tasks = await self.task_repository.get_user_tasks(user_id)
        if not tasks:
            raise TaskNotFoundError
        return [TaskSchema.model_validate(x) for x in tasks]

    async def get_user_tasks(
            self,
            user_id: int
    ) -> list[TaskSchema]:
        """
        Возвращает список задач, созданных указанным пользователем.
        :param user_id: Идентификатор пользователя.
        :raise TaskNotFoundError: Если задачи для обновления не существует.
        :return: Задачи пользователя.
        """
        if user_tasks := await self.task_cache_repository.get_user_tasks(user_id):
            pass
        else:
            if user_tasks := await self.task_repository.get_user_tasks(user_id):
                tasks_schema = [TaskSchema.model_validate(task) for task in user_tasks]
                await self.task_cache_repository.set_user_tasks(user_id, tasks_schema)
            raise TaskNotFoundError

        return user_tasks
