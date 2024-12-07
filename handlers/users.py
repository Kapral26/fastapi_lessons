from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from dependencies import get_user_service
from schemas import UserLoginSchema
from schemas.users import UserSchema
from service.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", response_model=UserLoginSchema)
async def create_user(
    body: UserSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserLoginSchema:
    """
    Создает нового пользователя.

    Описание:
    - Создает нового пользователя в базе данных.
    - Генерирует токен доступа для нового пользователя.
    - Возвращает данные пользователя в формате UserLoginSchema.

    Аргументы:
    - body: Данные пользователя в формате UserSchema.

    Возвращает:
    - Данные пользователя в формате UserLoginSchema.
    """
    try:
        create_user_result = await user_service.create_user(body.username, body.password)
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error))

    return create_user_result
