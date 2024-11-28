from typing import TypeVar, Sequence, Callable

from faker import Faker
from sqlalchemy import select, update, delete, insert, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import TaskModel, CategoryModel
from schemas.tasks import TaskCreateSchema

T = TypeVar(
        "T"
)


class TaskRepository:
    """
    Класс для работы с задачами в базе данных.

    Атрибуты:
    session_factory (Callable[[T], AsyncSession]): Фабрика асинхронных сессий.

    Методы:
    create_task(self, task_data: TaskSchema) -> None: Создает новую задачу.
    get_tasks(self) -> Sequence[TaskModel]: Получает список всех задач.
    update_task_name(self, task_id: int, new_name: str) -> type[TaskModel] | None: Обновляет имя задачи.
    get_task_by_name(self, name: str) -> TaskModel | None: Получает задачу по имени.
    get_task_by_id(self, task_id: int) -> TaskModel | None: Получает задачу по идентификатору.
    delete_task(self, task_id: int) -> None: Удаляет задачу.
    get_task_by_category_id(self, category_id: int) -> Sequence[TaskModel]: Получает задачи по идентификатору категории.
    get_task_by_category_name(self, category_name: str) -> Sequence[TaskModel]: Получает задачи по имени категории.
    insert_fake_data(self, num_tasks: int = 20) -> None: Вставляет фиктивные данные в базу данных.
    """

    def __init__(
            self,
            session_factory: Callable[[T], AsyncSession]
    ):
        self.session_factory = session_factory

    async def get_tasks(
            self
    ) -> Sequence[TaskModel]:
        """
        Получает список всех задач.

        Описание:
        - Выполняет запрос на выборку всех задач из базы данных.
        - Возвращает список моделей TaskModel.

        Возвращает:
        - Список моделей TaskModel.
        """
        async with self.session_factory() as session:
            query_result = await session.execute(
                    select(
                            TaskModel
                    )
            )
            tasks = query_result.scalars().all()
        return tasks

    async def create_task(
            self,
            task_data: TaskCreateSchema,
            user_id: int
    ) -> int:
        query = (
            insert(
                    TaskModel
            )
            .values(
                    **task_data.dict(),
                    user_id=user_id
            )
            .returning(
                    TaskModel.id
            )
        )
        async with self.session_factory() as session:
            task_id = (await session.execute(
                    query
            )).scalar_one_or_none()
            await session.commit()
            return task_id

    async def update_task_name(
            self,
            task_id: int,
            new_name: str,
            user_id: int
    ) -> TaskModel | None:
        """
        Обновляет имя задачи.

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
        async with self.session_factory() as session:
            query = (
                update(
                        TaskModel
                ).values(
                        name=new_name,
                        user_id=user_id
                ).where(
                        and_(
                                TaskModel.id == task_id,
                                TaskModel.user_id == user_id
                        )
                )
            )
            await session.execute(
                    query
            )
            await session.commit()
            task = await session.get(
                    TaskModel,
                    task_id
            )
            return task

    async def get_task_by_name(
            self,
            name: str
    ) -> TaskModel | None:
        """
        Получение задачи по имени.

        Описание:
        - Выполняет запрос на выборку задачи по имени.
        - Возвращает первую найденную задачу или None, если задача не найдена.

        Аргументы:
        - name: Имя задачи.

        Возвращает:
        - Модель TaskModel, если задача найдена.
        - None, если задача не найдена.
        """
        async with self.session_factory() as session:
            query_result = await session.execute(
                    select(
                            TaskModel
                    ).where(
                            TaskModel.name == name
                    )
            )

            task = query_result.scalar_one_or_none()

        return task

    async def get_task_by_id(
            self,
            task_id: int
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
        async with self.session_factory() as session:
            query_result = await session.execute(
                    select(
                            TaskModel
                    ).where(
                            TaskModel.id == task_id
                    )
            )
            task = query_result.scalar_one_or_none()
        return task

    async def get_task_by_user(
            self,
            user_id: int,
            task_id: int
    ) -> TaskModel | None:
        async with self.session_factory() as session:
            query_result = await session.execute(
                    select(
                            TaskModel
                    )
                    .where(
                            and_(
                                    TaskModel.id == task_id,
                                    TaskModel.user_id == user_id
                            )
                    )
            )
            task = query_result.scalar_one_or_none()
        return task

    async def get_user_tasks(
            self,
            user_id: int,
    ) -> list[TaskModel] | None:
        async with self.session_factory() as session:
            query_result = await session.execute(
                    select(
                            TaskModel
                    )
                    .where(
                            TaskModel.user_id == user_id
                    )
            )
            user_tasks = query_result.scalars().all()
        return user_tasks

    async def delete_task(
            self,
            task_id: int
    ) -> int:
        """
        Удаление задачи.

        Описание:
        - Удаляет задачу из базы данных.

        Аргументы:
        - task_id: Идентификатор задачи.
        """
        async with self.session_factory() as session:
            result = await session.execute(
                    delete(
                            TaskModel
                    ).where(
                            TaskModel.id == task_id
                    )
            )
            await session.commit()
            return result.rowcount

    async def get_task_by_category_id(
            self,
            category_id: int
    ) -> Sequence[TaskModel]:
        """
        Получение задач по идентификатору категории.

        Описание:
        - Выполняет запрос на выборку задач по идентификатору категории.
        - Возвращает список моделей TaskModel.

        Аргументы:
        - category_id: Идентификатор категории.

        Возвращает:
        - Список моделей TaskModel.
        """
        async with self.session_factory() as session:
            query_result = await session.execute(
                    select(
                            TaskModel
                    )
                    .options(
                            selectinload(
                                    TaskModel.category
                            )
                    )
                    .where(
                            TaskModel.category_id == category_id
                    )
            )
            tasks = query_result.scalars().all()
        return tasks

    async def get_task_by_category_name(
            self,
            category_name: str
    ) -> Sequence[TaskModel]:
        """
        Получение задач по имени категории.

        Описание:
        - Выполняет запрос на выборку задач по имени категории.
        - Возвращает список моделей TaskModel.

        Аргументы:
        - category_name: Имя категории.

        Возвращает:
        - Список моделей TaskModel.
        """
        async with self.session_factory() as session:
            query = (
                select(
                        TaskModel
                )
                .options(
                        selectinload(
                                TaskModel.category
                        )
                )
                .where(
                        TaskModel.category.has(
                                CategoryModel.name == category_name
                        )
                )
            )
            query_result = await session.execute(
                    query
            )
            tasks = query_result.scalars().all()
        return tasks

    async def insert_fake_data(
            self,
            num_tasks: int = 20
    ) -> None:
        """
        Вставляет фиктивные данные в базу данных.

        Описание:
        - Удаляет все задачи и категории из базы данных.
        - Создает фиктивные категории и задачи.
        - Добавляет задачи в базу данных.

        Аргументы:
        - num_tasks: Количество фиктивных задач для вставки (по умолчанию 20).
        """
        fake = Faker()
        async with self.session_factory() as session:
            await session.execute(
                    delete(
                            TaskModel
                    )
            )
            await session.execute(
                    delete(
                            CategoryModel
                    )
            )
            await session.commit()

            category_ids = []
            for _ in range(
                    5
            ):
                category = CategoryModel(
                        name=fake.job()
                )
                session.add(
                        category
                )
                await session.flush()
                category_ids.append(
                        category.id
                )
            await session.commit()

            for _ in range(
                    num_tasks
            ):
                try:
                    task = TaskModel(
                            name=fake.company(),
                            pomodoro_count=fake.random_int(
                                    min=5,
                                    max=15
                            ),
                            category_id=fake.random_element(
                                    elements=category_ids
                            ),
                    )
                    session.add(
                            task
                    )
                except Exception:  # noqa: S112
                    continue
            await session.commit()
            await session.close()
