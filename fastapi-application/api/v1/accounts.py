from fastapi import APIRouter, Depends
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
    new_account = Account(
        user_id=user.id,
        account_name=account_data.account_name,
        account_number=Account.generate_account_number(),
    )

    db.add(new_account)
    await db.commit()
    await db.refresh(new_account)
    return new_account
