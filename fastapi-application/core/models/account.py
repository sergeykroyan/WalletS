import uuid
from decimal import Decimal
from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import Integer, DateTime, func, Numeric, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.models import Base
from core.models.mixins.id import IdIntPkMixin

if TYPE_CHECKING:
    from .transaction import Transaction
    from .invoice import Invoice


class Account(Base, IdIntPkMixin):
    account_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    account_number: Mapped[str] = mapped_column(
        String(12), unique=True, index=True, nullable=False
    )
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
        "Invoice", foreign_keys="Invoice.account_id", back_populates="account"
    )
    received_invoices: Mapped[List["Invoice"]] = relationship(
        "Invoice",
        foreign_keys="Invoice.receiver_account_id",
        back_populates="receiver_account",
    )

    @staticmethod
    def generate_account_number():
        """Generate a unique 12-digit account number."""
        return str(uuid.uuid4().int)[:12]
