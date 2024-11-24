from collections.abc import Callable, Sequence
from typing import TypeVar

from faker import Faker
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.models.task_models import TaskModel, CategoryModel
from schemas.Tasks import TaskDTO

T = TypeVar("T")


class TaskRepository:
    def __init__(self, session_factory: Callable[[T], AsyncSession]):
        """
        Initialize a TaskRepository.

        :param session_factory: a callable that returns an instance of
            :class:`sqlalchemy.ext.asyncio.AsyncSession`.
        """
        self.session_factory = session_factory

    async def create_task(self, task_data: TaskDTO) -> None:
        """Создание задачи."""
        task_model = TaskModel(**task_data.dict())
        async with self.session_factory() as session:
            session.add(task_model)
            await session.commit()

    async def get_tasks(self) -> Sequence[TaskModel]:
        """
        Get all tasks.

        :return: a list of :class:`TaskModel` objects
        """
        async with self.session_factory() as session:
            query_result = await session.execute(select(TaskModel))
            tasks = query_result.scalars().all()
        return tasks

    async def update_task_name(self, task_id: int, new_name: str) -> type[TaskModel] | None:
        """Обновление задачи."""
        async with self.session_factory() as session:
            query = update(TaskModel).values(name=new_name).where(TaskModel.id == task_id)
            await session.execute(query)
            await session.commit()
            task = await session.get(TaskModel, task_id)
            return task

    async def get_task_by_name(self, name: str) -> TaskModel | None:
        """Получение задачи по имени."""
        async with self.session_factory() as session:
            query_result = await session.execute(select(TaskModel).where(TaskModel.name == name))

            task = query_result.scalar_one_or_none()

        return task

    async def get_task_by_id(self, task_id: int) -> TaskModel | None:
        """
        Get a task by its ID.

        :param task_id: the ID of the task to be retrieved
        :return: a :class:`TaskModel` object, or None if no task with the given
            ID exists
        """
        async with self.session_factory() as session:
            query_result = await session.execute(select(TaskModel).where(TaskModel.id == task_id))
            task = query_result.scalar_one_or_none()
        return task

    async def delete_task(self, task_id: int) -> None:
        """Удаление задачи."""
        async with self.session_factory() as session:
            await session.execute(delete(TaskModel).where(TaskModel.id == task_id))
            await session.commit()

    async def get_task_by_category_id(self, category_id: int) -> TaskModel | list[TaskModel] | None:
        """
        Get a task by its category ID.

        :param category_id: the ID of the category to be searched
        :return: a :class:`TaskModel` object, or a list of :class:`TaskModel` objects
            if there are multiple tasks with the same category ID, or None if no
            task with the given category ID exists
        """
        async with self.session_factory() as session:
            query_result = await session.execute(
                select(TaskModel).options(selectinload(TaskModel.category)).where(TaskModel.category_id == category_id)
            )
            tasks = query_result.scalars().all()
        return tasks

    async def get_task_by_category_name(self, category_name: str) -> TaskModel | list[TaskModel] | None:
        """
        Get a task by its category name.

        :param category_name: the name of the category to be searched
        :return: a :class:`TaskModel` object, or a list of :class:`TaskModel` objects
            if there are multiple tasks with the same category name, or None if no
            task with the given category name exists
        """
        async with self.session_factory() as session:
            query = (
                select(TaskModel)
                .options(selectinload(TaskModel.category))
                .where(TaskModel.category.has(CategoryModel.name == category_name))
            )
            query_result = await session.execute(query)
            tasks = query_result.scalars().all()
        return tasks

    async def insert_fake_data(self, num_tasks: int = 20) -> None:
        """Insert fake data into the tables."""
        fake = Faker()
        async with self.session_factory() as session:
            await session.execute(delete(TaskModel))
            await session.execute(delete(CategoryModel))
            await session.commit()

            category_ids = []
            for _ in range(5):
                category = CategoryModel(name=fake.job())
                session.add(category)
                await session.flush()
                category_ids.append(category.id)
            await session.commit()

            for _ in range(num_tasks):
                try:
                    task = TaskModel(
                        name=fake.company(),
                        pomodoro_count=fake.random_int(min=5, max=15),
                        category_id=fake.random_element(elements=category_ids),
                    )
                    session.add(task)
                except Exception:  # noqa: S112
                    continue
            await session.commit()
            await session.close()
