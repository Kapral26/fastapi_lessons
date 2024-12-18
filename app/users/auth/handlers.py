from typing import Annotated

from fastapi import APIRouter, Depends, Form

from app.dependencies import get_auth_service, UserGetterFromToken, get_token_payload
from app.settings.main_settings import Settings
from app.users.auth import AuthService
from app.users.auth.token.schemas import TokenResponseInfo
from app.users.users_profile import UserSchema

settings = Settings()

router = APIRouter(
        prefix="/auth",
        tags=["auth"]
)


@router.post("/login", response_model=TokenResponseInfo)
async def auth_user_jwt(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        username: str = Form(...),
        password: str = Form(...),
) -> TokenResponseInfo:
    valid_user = await auth_service.validate_user(username, password)
    user_tokens = await auth_service.user_login(valid_user)
    return user_tokens


#
@router.post(
        "/refresh",
        response_model=TokenResponseInfo,
        response_model_exclude_none=True
)
def refresh_user_jwt(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        user: UserSchema = Depends(UserGetterFromToken(settings.auth_jwt.refresh_token_type)),
):
    access_token = auth_service.create_access_token(user)
    return TokenResponseInfo(
            access_token=access_token,
    )


@router.get("/me")
def get_info_about_me(
        payload: dict = Depends(get_token_payload),
        user: UserSchema = Depends(UserGetterFromToken(settings.auth_jwt.access_token_type)),
):
    return {
        **user.dict(),
        "logged_in": payload["iat"],
    }
