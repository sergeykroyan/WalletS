from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import Column, Boolean
from sqlalchemy.orm import Mapped, relationship

from .base import Base
from .mixins.id import IdIntPkMixin

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from .invoice import Invoice


class User(Base, IdIntPkMixin, SQLAlchemyBaseUserTable[int]):
    is_admin = Column(Boolean, default=False)

    reviewed_invoices: Mapped[list["Invoice"]] = relationship(
        "Invoice", back_populates="reviewer"
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
