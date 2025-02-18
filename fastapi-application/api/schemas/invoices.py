from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime
from typing import Optional

from api.schemas.accounts import AccountResponse
from core.models.invoice import InvoiceStatus, InvoiceCategory


class BaseInvoiceSchema(BaseModel):
    amount: Decimal = Field(..., gt=0)


class DepositInvoiceCreate(BaseInvoiceSchema):
    account_number: str


class WithdrawInvoiceCreate(BaseInvoiceSchema):
    account_number: str


class InternalTransferInvoiceCreate(BaseInvoiceSchema):
    sender_account_number: str
    receiver_account_number: str


class ExternalTransferInvoiceCreate(BaseInvoiceSchema):
    sender_account_number: str
    receiver_account_number: str


class InvoiceStatusUpdate(BaseModel):
    status: InvoiceStatus


class BaseInvoiceResponse(BaseModel):
    id: int
    amount: Decimal
    status: InvoiceStatus
    category: InvoiceCategory
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class InvoiceResponse(BaseInvoiceResponse):
    account: AccountResponse


class TransferInvoiceResponse(BaseInvoiceResponse):
    account: AccountResponse
    receiver_account: AccountResponse
