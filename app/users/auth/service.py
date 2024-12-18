from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING

import bcrypt

from app.settings.main_settings import Settings
from app.users.auth.exceptions import UnauthorisedError, UserIsNotActiveError
from app.users.auth.token.schemas import TokenResponseInfo
from app.users.users_profile import UserSchema

if TYPE_CHECKING:
    from app.users.auth.token.service import TokenService
    from app.users.users_profile import UserRepository


@dataclass
class AuthService:
    """
    Класс для работы с аутентификацией пользователей.

    Атрибуты:
    user_repository (UserRepository): Экземпляр класса UserRepository, который используется
     для работы с пользователями в базе данных.
    settings (Settings): Экземпляр класса Settings, который содержит настройки приложения.

    Методы:
    user_login(self, username: str, password: str) -> UserLoginSchema | None: Пытается выполнить вход пользователя
     с указанными данными.
    _validate_user(self, user: UserProfile, password: str) -> None: Проверяет, что пользователь существует
     и пароль верный.
    generate_access_token(self, user_id: int) -> str: Генерирует токен доступа для пользователя.
    """

    user_repository: "UserRepository"
    settings: Settings
    token_service: "TokenService"

    async def user_login(
            self,
            user: UserSchema
    ) -> TokenResponseInfo | None:
        return TokenResponseInfo(
                access_token=self.create_access_token(user),
                refresh_token=self.create_refresh_token(user)
        )

    async def validate_user(
            self,
            username: str,
            password: str
    ) -> UserSchema:
        """
        Проверяет корректность имени пользователя и пароля.

        :param username: Имя пользователя из формы.
        :param password: Пароль из формы.
        :return: Данные пользователя при успешной проверке.
        :raises UnauthorisedError: Если имя пользователя или пароль неверны.
        :raises UserIsNotActiveError: Если пользователь неактивен.
        """
        if not (user := await self.user_repository.get_user_by_name(username)):
            raise UnauthorisedError
        if not self.validate_password(password, user.password):
            raise UnauthorisedError
        if not user.active:
            raise UserIsNotActiveError
        return UserSchema.model_validate(user)

    def create_access_token(self, user: UserSchema) -> str:
        """
        Создает JWT-токен доступа для указанного пользователя.

        :param user: Объект пользователя, для которого создается токен.
        :return: Сгенерированный JWT-токен доступа.
        """
        jwt_payload = {
            "sub": str(user.id),  # Обычно используется идентификатор пользователя.
            "username": user.username,
            "email": user.email,
        }

        return self.token_service.create_jwt(
                self.settings.auth_jwt.access_token_type,
                jwt_payload
        )

    def create_refresh_token(self, user: UserSchema) -> str:
        """
        Создает JWT-токен обновления для указанного пользователя.

        :param user: Объект пользователя, для которого создается токен.
        :return: Сгенерированный JWT-токен обновления.
        """
        jwt_payload = {
            "sub": str(user.id),  # Для refresh токенв достаточно будет передавать id пользователя.
        }

        return self.token_service.create_jwt(
                self.settings.auth_jwt.refresh_token_type,
                jwt_payload,
                expire_timedelta=timedelta(days=self.settings.auth_jwt.refresh_token_expire_days)
        )

    @staticmethod
    def hash_password(password: str) -> bytes:
        """
        Хэширует пароль с использованием алгоритма bcrypt.

        :param password: Оригинальный пароль в виде строки.
        :return: Хэшированный пароль в виде байтов.
        """
        salt = bcrypt.gensalt()
        pwd_bytes = password.encode()
        return bcrypt.hashpw(pwd_bytes, salt)

    @staticmethod
    def validate_password(
            password: str,
            hashed_password: bytes
    ) -> bool:
        """
        Проверяет, совпадает ли предоставленный пароль с хэшированным значением.

        :param password: Оригинальный пароль.
        :param hashed_password: Хэшированный пароль.
        :return: True, если пароли совпадают, иначе False.
        """
        return bcrypt.checkpw(
                password.encode(),
                hashed_password
        )
