from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from dependencies import get_auth_service
from exceptions import UserNotFoundError, UserInvalidError
from schemas import UserLoginSchema
from schemas.users import UserSchema
from service.auth_service import AuthService

router = APIRouter(
        prefix="/auth",
        tags=["auth"],
)


@router.post("/login", response_model=UserLoginSchema)
async def auth_user(
        body: UserSchema,
        user_repository: Annotated[AuthService, Depends(get_auth_service)],
) -> UserLoginSchema:
    """
    Аутентифицирует пользователя.

    Описание:
    - Пытается выполнить вход пользователя с указанными данными.
    - Если пользователь не найден, генерирует исключение UserNotFoundError.
    - Если пароль неверный, генерирует исключение UserInvalidError.
    - Возвращает данные пользователя в формате UserLoginSchema.

    Аргументы:
    - body: Данные пользователя в формате UserSchema.

    Возвращает:
    - Данные пользователя в формате UserLoginSchema.
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
