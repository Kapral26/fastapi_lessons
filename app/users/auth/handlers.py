from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.dependencies import get_auth_service
from app.exceptions import UserNotFoundError, UserInvalidError
from app.users.auth import UserLoginSchema, AuthService
from app.users.auth.token.schemas import TokenInfo
from app.users.users_profile.schemas import UserSchema

ouath2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login_new")

router = APIRouter(
        prefix="/auth",
        tags=["auth"],
        dependencies=[Depends(ouath2_bearer)]
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


@router.post("/login_new", response_model=TokenInfo)
def auth_user_jwt(
        user: UserSchema = Depends(validate_users),
        auth_service: AuthService = Depends(get_auth_service),
) -> TokenInfo:
    """
    Авторизует пользователя и возвращает JWT-токен.

    :param user: Данные пользователя, полученные через зависимость validate_users.
    :return: Информация о токене (TokenInfo).
    """
    access_token = auth_service.create_access_token(user)
    refresh_token = auth_service.create_refresh_token(user)
    return TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token,
    )


@router.post(
        "/refresh",
        response_model=TokenInfo,
        response_model_exclude_none=True
)
def refresh_user_jwt(
        user: UserSchema = Depends(
                UserGetterFromToken(settings.auth_jwt.refresh_token_type)
        ),
):
    """
    Перевыпускает access_token.

    :param user: Данные пользователя, полученные через зависимость validate_users.
    :return: Информация о токене (TokenInfo).

    handler ожидает токен refresh_token.
    """
    access_token = create_access_token(user)
    return TokenInfo(
            access_token=access_token,
    )


@router.get("/me")
def get_info_about_me(
        payload: dict = Depends(get_token_payload),
        user: UserSchema = Depends(
                UserGetterFromToken(settings.auth_jwt.access_token_type)
        ),
):
    """
    Возвращает информацию о текущем пользователе.

    :param payload: Полезная нагрузка из токена.
    :param user: Данные текущего активного пользователя.
    :return: Информация о пользователе с отметкой времени входа.
    """
    return {
        **user.dict(),
        "logged_in": payload["iat"],
    }
