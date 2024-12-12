from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from app.schemes import CheckoutType, Status

if TYPE_CHECKING:
    from .model import Model
    from .location import Location
    from .company import Company
    from .supplier import Supplier
    from .user import User
    from .asset_logs import AssetLogs


class Asset(Base):
    __tablename__ = "assets"

    name: Mapped[str] = mapped_column(nullable=True, unique=False)
    serial_number: Mapped[str] = mapped_column(nullable=False, unique=True)
    status: Mapped[Status] = mapped_column(nullable=False, default=Status.AVAILABLE)
    checkout_type: Mapped[CheckoutType] = mapped_column(nullable=True, default=None)
    purchase_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    purchase_cost: Mapped[float] = mapped_column(nullable=True, default=None)
    invoice_number: Mapped[str] = mapped_column(nullable=True, default=None)
    varrianty_expiration_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )
    notes: Mapped[str] = mapped_column(Text, nullable=True)

    model_id: Mapped[int] = mapped_column(ForeignKey("models.id"), nullable=True, default=None)
    model: Mapped["Model"] = relationship(back_populates="assets", lazy="joined")

    location_id: Mapped[int] = mapped_column(
        ForeignKey("locations.id"), nullable=True, default=None
    )
    location: Mapped["Location"] = relationship(back_populates="assets", lazy="joined")

    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=True, default=None)
    company: Mapped["Company"] = relationship(back_populates="assets", lazy="joined")

    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id"), nullable=True, default=None
    )
    supplier: Mapped["Supplier"] = relationship(back_populates="assets", lazy="joined")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True, default=None)
    user: Mapped["User"] = relationship(back_populates="assets", lazy="joined")

    asset_logs: Mapped[list["AssetLogs"]] = relationship(back_populates="asset", lazy="joined")

    @property
    def checkout_to(self):
        return self.user.email if self.user else None

    @property
    def supplier_name(self):
        return self.supplier.name if self.supplier else None

    @property
    def model_name(self):
        return self.model.name if self.model else None

    @property
    def location_name(self):
        return self.location.name if self.location else None

    @property
    def company_name(self):
        return self.company.name if self.company else None

    @property
    def manufacturer_name(self):
        return self.model.manufacturer.name if self.model and self.model.manufacturer else None
