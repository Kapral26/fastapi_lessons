from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base, intpk


class UserProfile(Base):
    """Модель пользователя."""

    __tablename__ = "user_profile"

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
