from pydantic import BaseModel, Field


class UserLoginSchema(BaseModel):
    """
    Модель данных для входа пользователя.

    Атрибуты:
    user_id (int): Идентификатор пользователя.
    access_token (str): Токен доступа.

    Класс Config:
    from_attributes (bool): Флаг, указывающий, что атрибуты модели должны быть получены из атрибутов класса.
    """

    user_id: int = Field(..., alias="id")
    access_token: str

    class Config:
        """
        Класс Config используется для настройки поведения модели.

        Атрибуты:
        from_attributes (bool): Флаг, указывающий, что атрибуты модели должны быть получены из атрибутов класса.
        """

        from_attributes = True


class UserSchema(BaseModel):
    """
    Модель данных для пользователя.

    Атрибуты:
    username (str): Имя пользователя.
    password (str): Пароль пользователя.

    Класс Config:
    from_attributes (bool): Флаг, указывающий, что атрибуты модели должны быть получены из атрибутов класса.
    """

    username: str
    password: str

    class Config:
        """
        Класс Config используется для настройки поведения модели.

        Атрибуты:
        from_attributes (bool): Флаг, указывающий, что атрибуты модели должны быть получены из атрибутов класса.
        """

        from_attributes = True
