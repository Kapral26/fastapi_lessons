from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING

from jose import jwt, JWTError

from app.exceptions import UserNotFoundError, UserInvalidError, TokenIsNotCorrectError
from app.settings.main_settings import Settings
from app.users.auth.schemas import UserLoginSchema
from app.users.users_profile import UserProfile, UserSchema

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
            username: str,
            password: str
    ) -> UserLoginSchema | None:
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
    async def _validate_user(
            user: UserProfile,
            password: str
    ) -> None:
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

    def generate_access_token(
            self,
            user_id: int
    ) -> str:
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

        token = jwt.encode(
                {
                    "user_id": user_id,
                    "exp": self.settings.jwt_expires
                },
                self.settings.jwt_secret_key.get_secret_value(),  # ключ шифрования.
                algorithm=self.settings.jwt_algorithm,  # Алгоритм шифрования.
        )

        return token

    def get_user_id_from_access_token(
            self,
            access_token: str
    ) -> int | None:
        """
        Функция для получения идентификатора пользователя из токена доступа.

        :param access_token: Токен доступа.
        :return: Идентификатор пользователя или None, если токен некорректен.
        :raises TokenIsNotCorrectError: Если токен некорректен.
        """
        try:
            payload = jwt.decode(
                    access_token,
                    self.settings.jwt_secret_key.get_secret_value(),
                    algorithms=[self.settings.jwt_algorithm],
            )
        except JWTError:
            raise TokenIsNotCorrectError
        return payload["user_id"]

    def create_access_token(self, user: UserSchema) -> str:
        """
        Создает JWT-токен доступа для указанного пользователя.

        :param user: Объект пользователя, для которого создается токен.
        :return: Сгенерированный JWT-токен доступа.
        """
        jwt_payload = {
            "sub": user.id,  # Обычно используется идентификатор пользователя.
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
            "sub": user.id,  # Для refresh токенв достаточно будет передавать id пользователя.
        }

        return self.token_service.create_jwt(
                self.settings.auth_jwt.refresh_token_type,
                jwt_payload,
                expire_timedelta=timedelta(days=self.settings.auth_jwt.refresh_token_expire_days)
        )
