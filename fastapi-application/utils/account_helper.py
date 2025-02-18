from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Account
from fastapi import HTTPException


async def get_account_by_number(
    db: AsyncSession, account_number: str, user_id: int = None, must_exist: bool = True
):
    """
    Fetches an account by account_number.
    - If `user_id` is provided, ensures the account belongs to the given user.
    - If `must_exist=True`, raises an HTTPException if the account is not found.
    """
    query = select(Account).filter(Account.account_number == account_number)

    if user_id:
        query = query.filter(Account.user_id == user_id)

    result = await db.execute(query)
    account = result.scalars().first()

    if must_exist and not account:
        raise HTTPException(status_code=400, detail="Account not found.")

    return account
