from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from dependencies import get_user_service
from schemas import UserLoginDTO
from schemas.users import UserModel
from service.user import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", response_model=UserLoginDTO)
async def create_user(
    body: UserModel,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserLoginDTO:
    """
    Создает нового пользователя.

    Описание:
    - Создает нового пользователя в базе данных.
    - Генерирует токен доступа для нового пользователя.
    - Возвращает данные пользователя в формате UserLoginDTO.

    Аргументы:
    - body: Данные пользователя в формате UserModel.

    Возвращает:
    - Данные пользователя в формате UserLoginDTO.
    """
    try:
        create_user_result = await user_service.create_user(body.username, body.password)
    except Exception as error:
        raise HTTPException(status_code=422, detail=str(error))

    return create_user_result
