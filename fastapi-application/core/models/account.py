from decimal import Decimal
from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import Integer, DateTime, func, Numeric, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.models import Base
from core.models.mixins.id import IdIntPkMixin

if TYPE_CHECKING:
    from .transaction import Transaction
    from .invoice import Invoice


class Account(Base, IdIntPkMixin):
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    balance: Mapped[Decimal] = mapped_column(
        Numeric(precision=12, scale=2), default=Decimal("0.00")
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    transactions_sent: Mapped[List["Transaction"]] = relationship(
        "Transaction",
        foreign_keys="Transaction.sender_account_id",
        back_populates="sender_account",
    )
    transactions_received: Mapped[List["Transaction"]] = relationship(
        "Transaction",
        foreign_keys="Transaction.receiver_account_id",
        back_populates="receiver_account",
    )
    invoices: Mapped[List["Invoice"]] = relationship(
        "Invoice", back_populates="account"
    )
