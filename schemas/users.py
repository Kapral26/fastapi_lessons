from pydantic import BaseModel, Field


class UserLoginDTO(BaseModel):
    """Модель логина пользователя."""

    user_id: int = Field(..., alias="id")
    access_token: str

    class Config:
        """Класс необходимый для преобразования ORM-объекта в модель."""

        from_attributes = True


class UserModel(BaseModel):
    """Модель логина пользователя."""

    username: str
    password: str

    class Config:
        """Класс необходимый для преобразования ORM-объекта в модель."""

        from_attributes = True
