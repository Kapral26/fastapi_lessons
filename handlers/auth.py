from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from dependencies import get_auth_service
from exceptions import UserNotFoundError, UserInvalidError
from schemas import UserLoginDTO
from schemas.users import UserModel
from service.auth import AuthService

router = APIRouter(
    # Префикс handler`а, чтобы ниже при регистрации к каждому не указывать
    prefix="/auth",
    # Теги handler`а
    tags=["auth"],
)


@router.post("/login", response_model=UserLoginDTO)
async def auth_user(
    body: UserModel,
    user_repository: Annotated[AuthService, Depends(get_auth_service)],
) -> UserLoginDTO:
    """Handler для авторизации пользователя."""
    try:
        auth_user = await user_repository.user_login(body.username, body.password)
    except UserNotFoundError as error:
        raise HTTPException(status_code=401, detail=error.detail)
    except UserInvalidError as error:
        raise HTTPException(status_code=401, detail=error.detail)

    return auth_user
