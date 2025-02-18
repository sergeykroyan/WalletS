from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.invoice import InvoiceCategory, Invoice, InvoiceStatus
from utils.account_helper import get_account_by_number


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
