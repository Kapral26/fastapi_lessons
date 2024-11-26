import datetime as dt
from dataclasses import dataclass
from datetime import timedelta
from typing import TYPE_CHECKING

from jose import jwt

from exceptions import UserNotFoundError, UserInvalidError
from models import UserProfile
from schemas import UserLoginDTO
from settings import Settings

if TYPE_CHECKING:
    from repository import UserRepository


@dataclass
class AuthService:
    """Сервис авторизации"""

    user_repository: "UserRepository"
    settings: Settings

    async def user_login(self, username: str, password: str) -> UserLoginDTO | None:
        """Авторизация пользователя."""
        user: UserProfile | None = await self.user_repository.get_user_by_name(username)

        await self._validate_user(user, password)

        user.access_token = self.generate_access_token(user.id)

        return UserLoginDTO.model_validate(user)

    @staticmethod
    async def _validate_user(user: UserProfile, password: str) -> None:
        if not user:
            raise UserNotFoundError

        if user.password != password:
            raise UserInvalidError

    def generate_access_token(self, user_id: int) -> str:
        """Генерация jwt токена."""
        # Время жизни токена
        expires_date_unix = (dt.datetime.utcnow() + timedelta(days=7)).timestamp()

        token = jwt.encode(
            {"user_id": user_id, "expire": expires_date_unix},
            self.settings.jwt_secret_key.get_secret_value(),  # ключ шифрования.
            algorithm=self.settings.jwt_algorithm,  # Алгоритм шифрования.
        )

        return token
