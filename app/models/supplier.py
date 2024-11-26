from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .model import Model
    from .asset import Asset


class Supplier(Base):
    __tablename__ = "suppliers"

    name: Mapped[str] = mapped_column(nullable=False, unique=False)
    url: Mapped[str] = mapped_column(nullable=True)
    support_url: Mapped[str] = mapped_column(nullable=True)
    support_phone: Mapped[str] = mapped_column(nullable=True)
    support_email: Mapped[str] = mapped_column(nullable=True)

    assets: Mapped[list["Asset"]] = relationship("Asset", lazy="joined")
