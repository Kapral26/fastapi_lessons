from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import UserProfile

T = TypeVar("T")


@dataclass
class UserRepository:
    session_factory: Callable[[T], AsyncSession]

    async def create_user(
        self, username: str, password: str
    ) -> UserProfile:
        """Создание пользователя."""
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
        """Получение пользователя."""
        query = select(UserProfile).where(UserProfile.id == user_id)
        async with self.session_factory() as session:
            query_result = await session.execute(query)
            user = query_result.scalars().first()
            return user

    async def get_user_by_name(self, username: str) -> UserProfile | None:
        """Авторизация пользователя."""
        query = select(UserProfile).where(UserProfile.username == username)
        async with self.session_factory() as session:
            # Сбрасываем кэш SQLAlchemy
            session.expire_all()
            query_result = await session.execute(query)
            user = query_result.scalar_one_or_none()
            return user
