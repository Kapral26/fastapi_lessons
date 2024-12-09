from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.database import Base, intpk


class UserProfile(Base):
    """
    Модель пользователя.

    Атрибуты:
    id (Mapped[intpk]): Идентификатор пользователя.
    username (Mapped[str]): Имя пользователя.
    password (Mapped[str]): Пароль пользователя.

    Методы:
    __init__(self, **kwargs): Инициализирует экземпляр класса.
    """

    __tablename__ = "user_profile"

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
