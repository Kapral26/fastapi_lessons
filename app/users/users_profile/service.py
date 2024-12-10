from dataclasses import dataclass
from typing import TYPE_CHECKING

from app.users.auth.exceptions import UserIsNotExistsError
from app.users.auth.schemas import UserLoginSchema
from app.users.users_profile import UserRepository, UserSchema

if TYPE_CHECKING:
    from app.users.users_profile import UserProfile
    from app.users.auth.service import AuthService


@dataclass
class UserService:
    """
    Класс для работы с пользователями.

    Атрибуты:
    user_repository (UserRepository): Экземпляр класса UserRepository,
     который используется для работы с пользователями в базе данных.
    token_service (AuthService): Экземпляр класса AuthService,
     который используется для работы с аутентификацией пользователей.

    Методы:
    create_user(self, username: str, password: str) -> UserLoginSchema: Создает нового пользователя.
    """

    user_repository: UserRepository
    auth_service: "AuthService"

    async def create_user(
            self,
            username: str,
            password: str,
            email: str | None = None
    ) -> UserLoginSchema:
        new_user: UserProfile = await self.user_repository.create_user(
                username,
                self.auth_service.hash_password(password),
                email
        )
        new_user: UserSchema = UserSchema.model_validate(new_user)
        access_token = self.auth_service.create_access_token(new_user)
        refresh_token = self.auth_service.create_refresh_token(new_user)
        return UserLoginSchema(
                id=new_user.id,
                access_token=access_token,
                refresh_token=refresh_token
        )

    async def get_user_by_token_sub(self, payload: dict) -> UserSchema:
        """
        Функция для получения пользователя по sub (subject) из токена.

        :param payload: Пейлоад токена.
        :return: Объект пользователя.
        :raises UserIsNotExistsError: Если пользователь не найден.
        """
        user_id = int(payload["sub"])
        if not (current_user := await self.user_repository.get_user(user_id)):
            raise UserIsNotExistsError
        return UserSchema.model_validate(current_user)
