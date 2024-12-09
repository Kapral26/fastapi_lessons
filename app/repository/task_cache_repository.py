import json

from redis import asyncio as Redis  # noqa: N812

from app.schemas.tasks import TaskSchema


class TaskCacheRepository:
    """
    Класс для работы с кэшем задач в Redis.

    Атрибуты:
    redis (Redis): Объект подключения к Redis.

    Методы:
    get_tasks(self) -> list[TaskSchema] | None: Получает список задач из Redis.
    set_tasks(self, tasks: list[TaskSchema]) -> None: Сохраняет список задач в Redis.
    """

    def __init__(
            self,
            redis_session: Redis
    ):
        self.redis = redis_session

    async def get_tasks(
            self
    ) -> list[TaskSchema] | None:
        """
        Получает список задач из Redis.

        Описание:
        - Использует Redis pipeline для выполнения нескольких команд.
        - Запрашивает весь список задач, хранящихся в ключе "tasks" (диапазон от 0 до -1 означает "все элементы").
        - Преобразует каждый элемент из сохраненного JSON-формата в объект TaskSchema.

        Возвращает:
        - Список объектов TaskSchema, если данные найдены.
        - None, если список пуст или ключ отсутствует.
        """
        if not self.redis.exists("tasks"):
            return None

        async with self.redis.pipeline() as pipe:
            # Получить список задач из Redis

            await pipe.lrange("tasks", 0, -1)
            # Выполнить команды в pipeline
            response = await pipe.execute()
            # pipe.execute возвращает байтовое представление объектов,
            # поэтому нужно преобразовать в строки, потом уже в json и только после этого в Модель
            tasks = [
                TaskSchema.model_validate(json.loads(x.decode("utf8")))
                for x in response[0]
            ]
            return tasks

    async def set_tasks(
            self,
            tasks: list[TaskSchema]
    ) -> None:
        """
        Сохраняет список задач в Redis.

        Описание:
        - Удаляет текущий список задач (если он существует) в ключе "tasks".
        - Добавляет новый список задач, сериализованный в формат JSON.
        - Использует Redis pipeline для выполнения операций атомарно.

        Аргументы:
        - tasks: Список объектов TaskSchema, которые нужно сохранить.
        """
        # Сериализовать задачи в JSON для хранения в Redis
        tasks_json = [x.json() for x in tasks]
        async with self.redis.pipeline() as pipe:
            # Удалить старые задачи, если они существуют
            await pipe.delete("tasks")
            # Добавить новый список задач в Redis (в виде JSON-строк)
            await pipe.lpush("tasks", *tasks_json)
            # Указываю время жизни
            await pipe.expire("tasks", 60)
            # Выполнить команды в pipeline
            await pipe.execute()

    async def delete_task(
            self,
            task_id: int
    ) -> None:
        """
        Удаляет задачу с указанным идентификатором из списка задач.

        :param task_id: Идентификатор задачи, которую нужно удалить.
        :raises TaskNotFoundError: Если задача с указанным идентификатором не найдена.
        """
        tasks = await self.get_tasks()
        if tasks:
            new_tasks = [task for task in tasks if task.id != task_id]
            if new_tasks:
                async with self.redis.pipeline() as pipe:
                    # Добавить новый список задач в Redis (в виде JSON-строк)
                    await pipe.lpush("tasks", *new_tasks)
                    # Указываю время жизни
                    await pipe.expire("tasks", 60)
                    # Выполнить команды в pipeline
                    await pipe.execute()

    async def get_user_tasks(
            self,
            user_id: int
    ) -> list[TaskSchema] | None:
        """
        Возвращает список задач пользователя.

        :param user_id: Идентификатор пользователя.
        :raises TaskNotFoundError: Если задача с указанным идентификатором не найдена.
        """
        if not self.redis.exists(user_id):
            return None

        async with self.redis.pipeline() as pipe:
            # Получить список задач из Redis

            await pipe.lrange(user_id, 0, -1)
            # Выполнить команды в pipeline
            response = await pipe.execute()
            # pipe.execute возвращает байтовое представление объектов,
            # поэтому нужно преобразовать в строки, потом уже в json и только после этого в Модель
            tasks = [
                TaskSchema.model_validate(json.loads(x.decode("utf8")))
                for x in response[0]
            ]
            return tasks

    async def set_user_tasks(
            self,
            user_id: int,
            tasks: list[TaskSchema]
    ) -> None:
        """
        Сохраняет список задач в Redis.

        Описание:
        - Удаляет текущий список задач (если он существует) в ключе "tasks".
        - Добавляет новый список задач, сериализованный в формат JSON.
        - Использует Redis pipeline для выполнения операций атомарно.

        Аргументы:
        - tasks: Список объектов TaskSchema, которые нужно сохранить.
        """
        # Сериализовать задачи в JSON для хранения в Redis
        tasks_json = [x.json() for x in tasks]
        async with self.redis.pipeline() as pipe:
            # Удалить старые задачи, если они существуют
            await pipe.delete(user_id)
            # Добавить новый список задач в Redis (в виде JSON-строк)
            await pipe.lpush(user_id, *tasks_json)
            # Указываю время жизни
            await pipe.expire(user_id, 60)
            # Выполнить команды в pipeline
            await pipe.execute()
