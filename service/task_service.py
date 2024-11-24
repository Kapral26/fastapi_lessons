import dataclasses

from repository.task_cache_repository import TaskCacheRepository
from repository.task_repository import TaskRepository
from schemas.tasks import TaskDTO


@dataclasses.dataclass
class TaskService:
    """Класс для работы с задачами."""

    task_repository: TaskRepository
    task_cache_repository: TaskCacheRepository

    async def get_tasks(self) -> list[TaskDTO] | None:
        """Получение всех задач"""
        if all_tasks := self.task_cache_repository.get_tasks():
            pass
        else:
            all_tasks = await self.task_repository.get_tasks()
            tasks_schema = [TaskDTO.model_validate(task) for task in all_tasks]
            self.task_cache_repository.set_tasks(tasks_schema)

        return all_tasks
