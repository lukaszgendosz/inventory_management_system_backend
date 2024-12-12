from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .manufacturer import Manufacturer
    from .asset import Asset


class Model(Base):
    __tablename__ = "models"

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    model_number: Mapped[str] = mapped_column(nullable=True, unique=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)

    manufacturer_id: Mapped[int] = mapped_column(
        ForeignKey("manufacturers.id"), nullable=True, default=None
    )
    manufacturer: Mapped["Manufacturer"] = relationship(
        back_populates="models", lazy="joined", overlaps="manufacturer"
    )

    assets: Mapped[list["Asset"]] = relationship("Asset", backref="models", lazy="joined")
