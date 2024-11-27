import json

from redis import Redis

from schemas.tasks import TaskSchema


class TaskCacheRepository:
    """
    Класс для работы с кэшем задач в Redis.

    Атрибуты:
    redis (Redis): Объект подключения к Redis.

    Методы:
    get_tasks(self) -> list[TaskSchema] | None: Получает список задач из Redis.
    set_tasks(self, tasks: list[TaskSchema]) -> None: Сохраняет список задач в Redis.
    """

    def __init__(self, redis_session: Redis):
        self.redis = redis_session

    def get_tasks(self) -> list[TaskSchema] | None:
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
        with self.redis.pipeline() as pipe:
            # Получить список задач из Redis
            if not pipe.exists("tasks"):
                return None

            pipe.lrange("tasks", 0, -1)
            # Выполнить команды в pipeline
            response = pipe.execute()
            # pipe.execute возвращает байтовое представление объектов,
            # поэтому нужно преобразовать в строки, потом уже в json и только после этого в Модель
            tasks = [
                TaskSchema.model_validate(json.loads(x.decode("utf8")))
                for x in response[0]
            ]
            return tasks

    def set_tasks(self, tasks: list[TaskSchema]) -> None:
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
        with self.redis.pipeline() as pipe:
            # Удалить старые задачи, если они существуют
            pipe.delete("tasks")
            # Добавить новый список задач в Redis (в виде JSON-строк)
            pipe.lpush("tasks", *tasks_json)
            # Указываю время жизни
            pipe.expire("tasks", 60)
            # Выполнить команды в pipeline
            pipe.execute()
