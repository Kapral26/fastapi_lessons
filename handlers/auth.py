from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from dependencies import get_auth_service
from exceptions import UserNotFoundError, UserInvalidError
from schemas import UserLoginDTO
from schemas.users import UserModel
from service.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login", response_model=UserLoginDTO)
async def auth_user(
    body: UserModel,
    user_repository: Annotated[AuthService, Depends(get_auth_service)],
) -> UserLoginDTO:
    """
    Аутентифицирует пользователя.

    Описание:
    - Пытается выполнить вход пользователя с указанными данными.
    - Если пользователь не найден, генерирует исключение UserNotFoundError.
    - Если пароль неверный, генерирует исключение UserInvalidError.
    - Возвращает данные пользователя в формате UserLoginDTO.

    Аргументы:
    - body: Данные пользователя в формате UserModel.

    Возвращает:
    - Данные пользователя в формате UserLoginDTO.
    """
    try:
        user_login_result = await user_repository.user_login(
            body.username, body.password
        )
    except UserNotFoundError as error:
        raise HTTPException(status_code=401, detail=error.detail)
    except UserInvalidError as error:
        raise HTTPException(status_code=401, detail=error.detail)

    return user_login_result
