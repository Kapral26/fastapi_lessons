import datetime as dt
from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING

from jose import jwt, JWTError

from exceptions import UserNotFoundError, UserInvalidError, TokenExpiredError, TokenIsNotCorrectError
from models import UserProfile
from schemas import UserLoginSchema
from settings import Settings

if TYPE_CHECKING:
    from repository import UserRepository


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

    async def user_login(self, username: str, password: str) -> UserLoginSchema | None:
        """
        Пытается выполнить вход пользователя с указанными данными.

        Описание:
        - Пытается получить пользователя по имени.
        - Если пользователь не найден, генерирует исключение UserNotFoundError.
        - Если пароль неверный, генерирует исключение UserInvalidError.
        - Генерирует токен доступа для пользователя.

        Аргументы:
        - username: Имя пользователя.
        - password: Пароль пользователя.

        Возвращает:
        - Данные пользователя в формате UserLoginSchema, если вход выполнен успешно.
        - None, если вход не выполнен.
        """
        user: UserProfile | None = await self.user_repository.get_user_by_name(username)

        await self._validate_user(user, password)

        user.access_token = self.generate_access_token(user.id)

        return UserLoginSchema.model_validate(user)

    @staticmethod
    async def _validate_user(user: UserProfile, password: str) -> None:
        """
        Проверяет, что пользователь существует и пароль верный.

        Описание:
        - Проверяет, что пользователь существует.
        - Проверяет, что пароль верный.

        Аргументы:
        - user: Пользователь.
        - password: Пароль пользователя.

        Возвращает:
        - None, если пользователь существует и пароль верный.
        - Исключение UserNotFoundError, если пользователь не найден.
        - Исключение UserInvalidError, если пароль неверный.
        """
        if not user:
            raise UserNotFoundError

        if user.password != password:
            raise UserInvalidError

    def generate_access_token(self, user_id: int) -> str:
        """
        Генерирует токен доступа для пользователя.

        Описание:
        - Генерирует токен доступа для пользователя.

        Аргументы:
        - user_id: Идентификатор пользователя.

        Возвращает:
        - Токен доступа для пользователя.
        """
        # Время жизни токена
        expires_date_unix = (dt.datetime.utcnow() + timedelta(days=7)).timestamp()

        token = jwt.encode(
            {"user_id": user_id, "expire": expires_date_unix},
            self.settings.jwt_secret_key.get_secret_value(),  # ключ шифрования.
            algorithm=self.settings.jwt_algorithm,  # Алгоритм шифрования.
        )

        return token

    def get_user_id_from_access_token(self, access_token: str) -> int | None:
        try:
            payload = jwt.decode(
                access_token,
                self.settings.jwt_secret_key.get_secret_value(),
                algorithms=[self.settings.jwt_algorithm],
            )
        except JWTError:
            raise TokenIsNotCorrectError
        if payload["expire"] < dt.datetime.utcnow().timestamp():
            raise TokenExpiredError
        return payload["user_id"]
