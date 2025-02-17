from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime
from core.models.invoice import InvoiceStatus, InvoiceCategory


class BaseInvoiceSchema(BaseModel):
    account_number: str
    amount: Decimal = Field(..., gt=0)


class DepositInvoiceCreate(BaseInvoiceSchema):
    pass


class WithdrawInvoiceCreate(BaseInvoiceSchema):
    pass


class InternalTransferInvoiceCreate(BaseModel):
    sender_account_number: str
    receiver_account_number: str
    amount: Decimal = Field(..., gt=0)


class ExternalTransferInvoiceCreate(BaseModel):
    sender_account_number: str
    receiver_account_number: str
    amount: Decimal = Field(..., gt=0)


class InvoiceStatusUpdate(BaseModel):
    status: InvoiceStatus


class InvoiceResponse(BaseInvoiceSchema):
    id: int
    status: InvoiceStatus
    category: InvoiceCategory
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
