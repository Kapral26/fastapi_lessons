from dataclasses import dataclass
from typing import TYPE_CHECKING

from repository import UserRepository
from schemas import UserLoginSchema

if TYPE_CHECKING:
    from models import UserProfile
    from service.auth_service import AuthService


@dataclass
class UserService:
    """
    Класс для работы с пользователями.

    Атрибуты:
    user_repository (UserRepository): Экземпляр класса UserRepository,
     который используется для работы с пользователями в базе данных.
    auth_service (AuthService): Экземпляр класса AuthService,
     который используется для работы с аутентификацией пользователей.

    Методы:
    create_user(self, username: str, password: str) -> UserLoginSchema: Создает нового пользователя.
    """

    user_repository: UserRepository
    auth_service: "AuthService"

    async def create_user(self, username: str, password: str) -> UserLoginSchema:
        """
        Создает нового пользователя.

        Описание:
        - Создает нового пользователя в базе данных.
        - Генерирует токен доступа для нового пользователя.
        - Возвращает данные пользователя в формате UserLoginSchema.

        Аргументы:
        - username: Имя пользователя.
        - password: Пароль пользователя.

        Возвращает:
        - Данные пользователя в формате UserLoginSchema.
        """
        new_user: UserProfile = await self.user_repository.create_user(
            username, password
        )
        access_token = self.auth_service.generate_access_token(new_user.id)
        return UserLoginSchema(user_id=new_user.id, access_token=access_token)
