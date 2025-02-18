from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.config import settings
from core.models.invoice import InvoiceStatus, InvoiceCategory
from core.models import db_helper, Invoice, Account
from utils.account_helper import get_account_by_number
from utils.invoice_helper import create_transfer_invoice
from utils.transaction_helper import create_transaction_from_invoice
from .fastapi_users import current_user

from api.schemas.invoices import (
    DepositInvoiceCreate,
    WithdrawInvoiceCreate,
    InternalTransferInvoiceCreate,
    ExternalTransferInvoiceCreate,
    InvoiceResponse,
    TransferInvoiceResponse,
    InvoiceStatusUpdate,
    InvoiceListResponse,
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


@router.get("/pending/", response_model=InvoiceListResponse)
async def get_pending_invoices(
    db: AsyncSession = Depends(db_helper.session_getter),
    user=Depends(current_user),
    limit: int = Query(10, gt=0, le=100),
    offset: int = Query(0, ge=0),
):
    """Admin-only endpoint to fetch all pending invoices."""
    if not user.is_admin:
        raise HTTPException(
            status_code=403, detail="Only admins can view pending invoices."
        )

    result = await db.execute(
        select(Invoice)
        .options(joinedload(Invoice.account), joinedload(Invoice.receiver_account))
        .filter(Invoice.status == InvoiceStatus.pending)
        .order_by(Invoice.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    invoices = result.scalars().all()
    return {"total": len(invoices), "invoices": invoices}


@router.patch("/{invoice_id}/status/", response_model=InvoiceResponse)
async def update_invoice_status(
    invoice_id: int,
    update_data: InvoiceStatusUpdate,
    db: AsyncSession = Depends(db_helper.session_getter),
    user=Depends(current_user),
):
    if not user.is_admin:
        raise HTTPException(
            status_code=403, detail="Only admins can approve/reject invoices."
        )

    result = await db.execute(
        select(Invoice)
        .options(joinedload(Invoice.account), joinedload(Invoice.receiver_account))
        .filter(Invoice.id == invoice_id)
    )
    invoice = result.scalars().first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found.")

    if invoice.status != InvoiceStatus.pending:
        raise HTTPException(
            status_code=400,
            detail="Only pending invoices can be updated.",
        )

    if update_data.status not in [InvoiceStatus.approved, InvoiceStatus.declined]:
        raise HTTPException(
            status_code=400,
            detail="Only 'approved' or 'declined' statuses are allowed.",
        )

    account_result = await db.execute(
        select(Account).filter(Account.id == invoice.account_id)
    )
    account = account_result.scalars().first()

    if not account:
        raise HTTPException(status_code=400, detail="Account not found.")

    if account.user_id == user.id:
        raise HTTPException(
            status_code=403, detail="You cannot approve your own invoice."
        )

    invoice.status = update_data.status
    invoice.reviewed_by = user.id

    if invoice.status == InvoiceStatus.approved:
        await create_transaction_from_invoice(invoice, db)

    await db.commit()
    await db.refresh(invoice)
    return invoice
