import enum
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, DateTime, func, Enum, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.models import Base
from core.models.mixins.id import IdIntPkMixin

if TYPE_CHECKING:
    from .invoice import Invoice


class TransactionStatus(enum.Enum):
    initiated = "initiated"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class TransactionCategory(enum.Enum):
    deposit = "deposit"
    transfer = "transfer"
    withdrawal = "withdrawal"


class Transaction(Base, IdIntPkMixin):
    sender_account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id"), nullable=True
    )
    receiver_account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id"), nullable=True
    )
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id"), nullable=True)
    amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=12, scale=2), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    status: Mapped[TransactionStatus] = mapped_column(
        Enum(TransactionStatus), default=TransactionStatus.initiated, nullable=False
    )
    category: Mapped[TransactionCategory] = mapped_column(
        Enum(TransactionCategory), default=TransactionCategory.deposit, nullable=False
    )
    sender_account = relationship(
        "Account", foreign_keys=[sender_account_id], back_populates="transactions_sent"
    )
    receiver_account = relationship(
        "Account",
        foreign_keys=[receiver_account_id],
        back_populates="transactions_received",
    )
    invoice: Mapped["Invoice"] = relationship("Invoice", back_populates="transactions")
