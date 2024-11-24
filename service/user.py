import secrets
import string
from dataclasses import dataclass

from repository import UserRepository
from schemas import UserLoginDTO


@dataclass
class UserService:
    user_repository: UserRepository

    async def create_user(self, username: str, password: str) -> UserLoginDTO:
        new_user = await self.user_repository.create_user(
            username, password, self._generate_access_token()
        )
        breakpoint()
        return UserLoginDTO.model_validate(new_user)

    @staticmethod
    def _generate_access_token(length: int = 20) -> str:
        """Генерация access token заданной длины.

        :param length: Длина access token (по умолчанию 20)
        :return: Строка access token
        """
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(length))
