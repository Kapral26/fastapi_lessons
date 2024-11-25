from dataclasses import dataclass

from exceptions import UserNotFoundError, UserInvalidError
from schemas import UserLoginDTO
from schemas.users import UserModel


@dataclass
class AuthService:
    user_repository: "UserRepository"

    async def user_login(self, username: str, password: str) -> UserLoginDTO | None:
        """Авторизация пользователя."""
        user = await self.user_repository.get_user_by_name(username)

        await self._validate_user(user, password)

        return UserLoginDTO.model_validate(user)

    @staticmethod
    async def _validate_user(user: UserModel, password: str) -> None:
        if not user:
            raise UserNotFoundError

        if user.password != password:
            raise UserInvalidError
