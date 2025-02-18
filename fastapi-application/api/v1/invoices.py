from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models.invoice import InvoiceStatus, InvoiceCategory
from core.models import db_helper, Invoice
from utils.account_helper import get_account_by_number
from .fastapi_users import current_user

from api.schemas.invoices import (
    DepositInvoiceCreate,
    WithdrawInvoiceCreate,
    InternalTransferInvoiceCreate,
    ExternalTransferInvoiceCreate,
    InvoiceResponse,
    TransferInvoiceResponse,
)

router = APIRouter(prefix=settings.api.v1.invoices, tags=["Invoices"])


@router.post("/deposit/", response_model=InvoiceResponse)
async def create_deposit_invoice(
    invoice_data: DepositInvoiceCreate,
    db: AsyncSession = Depends(db_helper.session_getter),
    user=Depends(current_user),
):
    account = await get_account_by_number(db, invoice_data.account_number, user.id)

    new_invoice = Invoice(
        account_id=account.id,
        receiver_account_id=None,
        amount=invoice_data.amount,
        status=InvoiceStatus.pending,
        category=InvoiceCategory.deposit,
    )

    db.add(new_invoice)
    await db.commit()
    await db.refresh(new_invoice, ["account"])
    return new_invoice


@router.post("/withdraw/", response_model=InvoiceResponse)
async def create_withdraw_invoice(
    invoice_data: WithdrawInvoiceCreate,
    db: AsyncSession = Depends(db_helper.session_getter),
    user=Depends(current_user),
):
    account = await get_account_by_number(db, invoice_data.account_number, user.id)

    if account.balance < invoice_data.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance.")

    new_invoice = Invoice(
        account_id=account.id,
        receiver_account_id=None,
        amount=invoice_data.amount,
        status=InvoiceStatus.pending,
        category=InvoiceCategory.withdrawal,
    )

    db.add(new_invoice)
    await db.commit()
    await db.refresh(new_invoice, ["account"])
    return new_invoice


async def create_transfer_invoice(
    invoice_data, category: InvoiceCategory, user, db: AsyncSession
):
    """Generic function to handle both internal & external transfers"""
    sender_account = await get_account_by_number(
        db, invoice_data.sender_account_number, user.id
    )
    receiver_account = await get_account_by_number(
        db, invoice_data.receiver_account_number
    )

    if sender_account.account_number == receiver_account.account_number:
        raise HTTPException(
            status_code=400, detail="Cannot transfer to the same account."
        )

    if category == InvoiceCategory.internal_transfer:
        if receiver_account.user_id != user.id:
            raise HTTPException(
                status_code=400,
                detail="For an internal transfer, the receiver's account must belong to the same user.",
            )
    elif category == InvoiceCategory.external_transfer:
        if receiver_account.user_id == user.id:
            raise HTTPException(
                status_code=400,
                detail="For an external transfer, the receiver's account must belong to a different user.",
            )

    new_invoice = Invoice(
        account_id=sender_account.id,
        receiver_account_id=receiver_account.id,
        amount=invoice_data.amount,
        status=InvoiceStatus.pending,
        category=category,
    )

    db.add(new_invoice)
    await db.commit()
    await db.refresh(new_invoice, ["account", "receiver_account"])
    return new_invoice


@router.post("/transfer/internal/", response_model=TransferInvoiceResponse)
async def create_internal_transfer_invoice(
    invoice_data: InternalTransferInvoiceCreate,
    db: AsyncSession = Depends(db_helper.session_getter),
    user=Depends(current_user),
):
    return await create_transfer_invoice(
        invoice_data, InvoiceCategory.internal_transfer, user, db
    )


@router.post("/transfer/external/", response_model=TransferInvoiceResponse)
async def create_external_transfer_invoice(
    invoice_data: ExternalTransferInvoiceCreate,
    db: AsyncSession = Depends(db_helper.session_getter),
    user=Depends(current_user),
):
    return await create_transfer_invoice(
        invoice_data, InvoiceCategory.external_transfer, user, db
    )
