from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime


class AccountCreate(BaseModel):
    account_name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="name must be between 3-50 characters",
    )


class AccountResponse(BaseModel):
    id: int
    user_id: int
    account_name: str
    account_number: str
    balance: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
