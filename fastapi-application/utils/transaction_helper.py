from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from core.models import Account, Invoice, Transaction
from core.models.invoice import InvoiceCategory, InvoiceStatus
from core.models.transaction import TransactionCategory, TransactionStatus


async def create_transaction_from_invoice(invoice: Invoice, db: AsyncSession):
    """Creates a transaction after an invoice is approved."""

    sender_account_result = await db.execute(
        select(Account).filter(Account.id == invoice.account_id)
    )
    sender_account = sender_account_result.scalars().first()

    receiver_account_result = await db.execute(
        select(Account).filter(Account.id == invoice.receiver_account_id)
    )
    receiver_account = (
        receiver_account_result.scalars().first()
        if invoice.receiver_account_id
        else None
    )

    if not sender_account:
        raise HTTPException(status_code=400, detail="Sender account not found.")

    sender_account_id, receiver_account_id, category = None, None, None

    if invoice.category == InvoiceCategory.deposit:
        receiver_account_id = invoice.account_id
        category = TransactionCategory.deposit
    elif invoice.category == InvoiceCategory.withdrawal:
        sender_account_id = invoice.account_id
        category = TransactionCategory.withdrawal
    elif invoice.category in [
        InvoiceCategory.internal_transfer,
        InvoiceCategory.external_transfer,
    ]:
        sender_account_id = invoice.account_id
        receiver_account_id = invoice.receiver_account_id
        category = TransactionCategory.transfer

    new_transaction = Transaction(
        sender_account_id=sender_account_id,
        receiver_account_id=receiver_account_id,
        invoice_id=invoice.id,
        amount=invoice.amount,
        status=TransactionStatus.completed,
        category=category,
    )

    db.add(new_transaction)

    if invoice.category == InvoiceCategory.deposit:
        sender_account.balance += invoice.amount
    elif invoice.category == InvoiceCategory.withdrawal:
        if sender_account.balance < invoice.amount:
            raise HTTPException(status_code=400, detail="Insufficient balance.")
        sender_account.balance -= invoice.amount
    elif invoice.category in [
        InvoiceCategory.internal_transfer,
        InvoiceCategory.external_transfer,
    ]:
        if sender_account.balance < invoice.amount:
            raise HTTPException(status_code=400, detail="Insufficient balance.")
        sender_account.balance -= invoice.amount
        if receiver_account:
            receiver_account.balance += invoice.amount

    await db.commit()
