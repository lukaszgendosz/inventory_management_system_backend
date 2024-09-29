from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .model import Model


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(nullable=False, unique=False)

    # models: Mapped[list['Model']] = relationship("Model", back_populates="categories")
