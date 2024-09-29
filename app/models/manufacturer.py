from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .model import Model


class Manufacturer(Base):
    __tablename__ = "manufacturers"

    name: Mapped[str] = mapped_column(nullable=False, unique=False)
    url: Mapped[str] = mapped_column(nullable=True)
    support_url: Mapped[str] = mapped_column(nullable=True)
    support_phone: Mapped[str] = mapped_column(nullable=True)
    support_email: Mapped[str] = mapped_column(nullable=True)

    models: Mapped[list["Model"]] = relationship("Model", backref="manufacturers")
