import enum
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, DateTime, func, Enum, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from core.models.mixins.id import IdIntPkMixin


if TYPE_CHECKING:
    from .account import Account
    from .transaction import Transaction
    from .user import User


class InvoiceStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    declined = "declined"


class InvoiceCategory(enum.Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"
    internal_transfer = "internal_transfer"
    external_transfer = "external_transfer"


class Invoice(Base, IdIntPkMixin):
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=12, scale=2), nullable=False
    )
    status: Mapped[InvoiceStatus] = mapped_column(
        Enum(InvoiceStatus), default=InvoiceStatus.pending, nullable=False
    )
    category: Mapped[InvoiceCategory] = mapped_column(
        Enum(InvoiceCategory), default=InvoiceCategory.deposit, nullable=False
    )
    reviewed_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    account: Mapped["Account"] = relationship("Account", back_populates="invoices")
    transaction: Mapped["Transaction"] = relationship(
        "Transaction", back_populates="invoice", uselist=False
    )
    reviewer: Mapped["User"] = relationship("User", back_populates="reviewed_invoices")
