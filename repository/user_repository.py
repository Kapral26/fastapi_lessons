from dataclasses import dataclass
from typing import TypeVar, Callable

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import UserProfile

T = TypeVar("T")


@dataclass
class UserRepository:
    """
    Класс для работы с пользователями в базе данных.

    Атрибуты:
    session_factory (Callable[[T], AsyncSession]): Фабрика асинхронных сессий.

    Методы:
    create_user(self, username: str, password: str) -> UserProfile: Создает нового пользователя.
    get_user(self, user_id: int) -> UserProfile | None: Получает пользователя по идентификатору.
    get_user_by_name(self, username: str) -> UserProfile | None: Получает пользователя по имени.
    """

    session_factory: Callable[[T], AsyncSession]

    async def create_user(self, username: str, password: str) -> UserProfile:
        """
        Создает нового пользователя.

        Описание:
        - Создает новую запись в базе данных с указанными именем и паролем.
        - Возвращает созданного пользователя.

        Аргументы:
        - username: Имя пользователя.
        - password: Пароль пользователя.

        Возвращает:
        - Созданного пользователя.
        """
        stmnt = (
            insert(UserProfile)
            .values(username=username, password=password)
            .returning(UserProfile.id)
        )

        async with self.session_factory() as session:
            query_result = await session.execute(stmnt)
            new_user_id = query_result.scalars().first()
            await session.commit()

        new_user = await self.get_user(new_user_id)
        return new_user

    async def get_user(self, user_id: int) -> UserProfile | None:
        """
        Получает пользователя по идентификатору.

        Описание:
        - Выполняет запрос на выборку пользователя по идентификатору.
        - Возвращает первого найденного пользователя или None, если пользователь не найден.

        Аргументы:
        - user_id: Идентификатор пользователя.

        Возвращает:
        - Найденного пользователя или None, если пользователь не найден.
        """
        query = select(UserProfile).where(UserProfile.id == user_id)
        async with self.session_factory() as session:
            query_result = await session.execute(query)
            user = query_result.scalars().first()
            return user

    async def get_user_by_name(self, username: str) -> UserProfile | None:
        """
        Получает пользователя по имени.

        Описание:
        - Выполняет запрос на выборку пользователя по имени.
        - Возвращает первого найденного пользователя или None, если пользователь не найден.

        Аргументы:
        - username: Имя пользователя.

        Возвращает:
        - Найденного пользователя или None, если пользователь не найден.
        """
        query = select(UserProfile).where(UserProfile.username == username)
        async with self.session_factory() as session:
            # Сбрасываем кэш SQLAlchemy
            session.expire_all()
            query_result = await session.execute(query)
            user = query_result.scalar_one_or_none()
            return user
