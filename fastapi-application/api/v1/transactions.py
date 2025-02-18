from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.config import settings
from core.models import Transaction, db_helper, Account
from core.models.transaction import TransactionCategory, TransactionStatus
from .fastapi_users import current_user
from api.schemas.transactions import TransactionListResponse

router = APIRouter(prefix=settings.api.v1.transactions, tags=["Transactions"])


@router.get("/", response_model=TransactionListResponse)
async def get_transactions(
    db: AsyncSession = Depends(db_helper.session_getter),
    user=Depends(current_user),
    limit: int = Query(10, gt=0, le=100),
    offset: int = Query(0, ge=0),
    status: Optional[TransactionStatus] = None,
    category: Optional[TransactionCategory] = None,
):
    query = select(Transaction).order_by(Transaction.created_at.desc())

    if not user.is_admin:
        account_result = await db.execute(
            select(Account.id).filter(Account.user_id == user.id)
        )
        user_account_ids = [account_id for (account_id,) in account_result.all()]

        if not user_account_ids:
            return {"total": 0, "transactions": []}

        # Filter transactions to only include those related to the user's accounts
        query = query.filter(
            (Transaction.sender_account_id.in_(user_account_ids))
            | (Transaction.receiver_account_id.in_(user_account_ids))
        )

    if status:
        query = query.filter(Transaction.status == status)

    if category:
        query = query.filter(Transaction.category == category)

    query = query.limit(limit).offset(offset)

    result = await db.execute(query)
    transactions = result.scalars().all()

    return {"total": len(transactions), "transactions": transactions}
