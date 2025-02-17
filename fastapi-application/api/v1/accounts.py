from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas.accounts import AccountCreate, AccountResponse
from core.config import settings
from .fastapi_users import current_user
from core.models import Account, db_helper

router = APIRouter(prefix=settings.api.v1.accounts, tags=["Accounts"])


@router.post("/", response_model=AccountResponse)
async def create_account(
    account_data: AccountCreate,
    db: AsyncSession = Depends(db_helper.session_getter),
    user=Depends(current_user),
):
    result = await db.execute(
        select(Account).filter(
            Account.user_id == user.id,
            Account.account_name == account_data.account_name,
        )
    )
    existing_account = result.scalars().first()

    if existing_account:
        raise HTTPException(
            status_code=400, detail="An account with this name already exists."
        )

    # Unlikely but possible, we check uniqueness to ensure no duplicate account numbers.
    while True:
        generated_number = Account.generate_account_number()

        result = await db.execute(
            select(Account).filter(Account.account_number == generated_number)
        )
        existing_number = result.scalars().first()

        if not existing_number:
            account_number = generated_number
            break

    new_account = Account(
        user_id=user.id,
        account_name=account_data.account_name,
        account_number=account_number,
    )

    db.add(new_account)
    await db.commit()
    await db.refresh(new_account)
    return new_account
