from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from dependencies import get_user_service
from schemas import UserLoginDTO
from schemas.users import UserModel
from service.user import UserService

router = APIRouter(
    # Префикс handler`а, чтобы ниже при регистрации к каждому не указывать
    prefix="/users",
    # Теги handler`а
    tags=["users"],
)


@router.post("/", response_model=UserLoginDTO)
async def create_user(
    body: UserModel,
    user_repository: Annotated[UserService, Depends(get_user_service)],
) -> UserLoginDTO:
    """Handler для создания пользователя."""
    try:
        create_user_result = await user_repository.create_user(
            body.username, body.password
        )
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error))

    return create_user_result
