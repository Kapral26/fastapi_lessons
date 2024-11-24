from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base
from settings import Settings

settings = Settings()

intpk = Annotated[int, mapped_column(primary_key=True)]


class CategoryModel(Base):
    """Модель категории."""

    __tablename__ = "category"

    id: Mapped[intpk]
    name: Mapped[str]
    type: Mapped[str | None]
    tasks: Mapped[list["TaskModel"]] = relationship(
        back_populates="category",
    )


class TaskModel(Base):
    """Модель задачи."""

    __tablename__ = "tasks"

    id: Mapped[intpk]
    name: Mapped[str]
    pomodoro_count: Mapped[int]
    category_id: Mapped[int] = mapped_column(
        ForeignKey(
            "category.id",
            ondelete="SET NULL",
        )
    )

    category: Mapped[CategoryModel] = relationship(
        back_populates="tasks",
    )


class UserModel(Base):
    """Модель пользователя."""

    __tablename__ = "user"

    id: Mapped[intpk]
    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
