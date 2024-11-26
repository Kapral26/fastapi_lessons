from dataclasses import dataclass
from typing import TYPE_CHECKING

from repository import UserRepository
from schemas import UserLoginDTO

if TYPE_CHECKING:
    from models import UserProfile
    from service.auth import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: "AuthService"

    async def create_user(self, username: str, password: str) -> UserLoginDTO:
        """Создание нового пользователя."""
        new_user: UserProfile = await self.user_repository.create_user(
            username, password
        )
        access_token = self.auth_service.generate_access_token(new_user.id)
        return UserLoginDTO(user_id=new_user.id, access_token=access_token)
