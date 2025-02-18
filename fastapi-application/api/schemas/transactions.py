from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from core.models.transaction import TransactionStatus, TransactionCategory
from typing import Optional, List


class TransactionResponse(BaseModel):
    id: int
    sender_account_id: Optional[int] = None
    receiver_account_id: Optional[int] = None
    invoice_id: Optional[int] = None
    amount: Decimal
    created_at: datetime
    status: TransactionStatus
    category: TransactionCategory

    model_config = {"from_attributes": True}


class TransactionListResponse(BaseModel):
    total: int
    transactions: List[TransactionResponse]
