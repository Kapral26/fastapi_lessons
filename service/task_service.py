from dataclasses import dataclass

from repository.task_cache_repository import TaskCacheRepository
from repository.task_repository import TaskRepository
from schemas.tasks import TaskDTO


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
    get_tasks(self) -> list[TaskDTO] | None: Получает список задач.
    """

    task_repository: TaskRepository
    task_cache_repository: TaskCacheRepository

    async def get_tasks(self) -> list[TaskDTO] | None:
        """
        Получает список задач.

        Описание:
        - Пытается получить список задач из кэша.
        - Если список задач не найден в кэше, получает список задач из базы данных.
        - Сохраняет список задач в кэш.

        Возвращает:
        - Список задач в формате TaskDTO, если задачи найдены.
        - None, если список задач пуст или ключ отсутствует.
        """
        if all_tasks := self.task_cache_repository.get_tasks():
            pass
        else:
            all_tasks = await self.task_repository.get_tasks()
            tasks_schema = [TaskDTO.model_validate(task) for task in all_tasks]
            self.task_cache_repository.set_tasks(tasks_schema)

        return all_tasks
