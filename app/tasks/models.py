from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base, intpk
from app.settings.main_settings import Settings

settings = Settings()


class CategoryModel(Base):
    """
    Модель категории.

    Атрибуты:
    id (Mapped[intpk]): Идентификатор категории.
    name (Mapped[str]): Имя категории.
    type (Mapped[str | None]): Тип категории.
    tasks (Mapped[list["TaskModel"]]): Список задач, связанных с этой категорией.

    Методы:
    __init__(self, **kwargs): Инициализирует экземпляр класса.
    """

    __tablename__ = "category"

    id: Mapped[intpk]
    name: Mapped[str]
    type: Mapped[str | None]
    tasks: Mapped[list["TaskModel"]] = relationship(
            back_populates="category",
    )


class TaskModel(Base):
    """
    Модель задачи.

    Атрибуты:
    id (Mapped[intpk]): Идентификатор задачи.
    name (Mapped[str]): Имя задачи.
    pomodoro_count (Mapped[int]): Количество помидоров.
    category_id (Mapped[int]): Идентификатор категории.
    category (Mapped[CategoryModel]): Категория, к которой относится задача.

    Методы:
    __init__(self, **kwargs): Инициализирует экземпляр класса.
    """

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
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id"), nullable=False)

    category: Mapped[CategoryModel] = relationship(
            back_populates="tasks",
    )

    # Дополнительные параметры модели
    __table_args__ = (
        # Индекс на поле name
        Index(
                "name_idx",
                "name",
                "user_id",
                unique=True
        ),
    )
