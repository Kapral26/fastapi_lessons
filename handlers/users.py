from typing import Annotated

from fastapi import APIRouter, Depends

from dependencies import get_user_service
from models import UserProfile
from schemas import UserLoginDTO
from service.user import UserService

router = APIRouter(
    # Префикс handler`а, чтобы ниже при регистрации к каждому не указывать
    prefix="/users",
    # Теги handler`а
    tags=["users"],
)


@router.post("/", response_model=UserLoginDTO)
async def create_user(
    username: str,
    password: str,
    user_repository: Annotated[UserService, Depends(get_user_service)],
) -> UserProfile:
    """Handler для создания пользователя."""
    create_user_result = await user_repository.create_user(username, password)
    return create_user_result
