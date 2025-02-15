from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import Column, Boolean
from sqlalchemy.ext.asyncio import AsyncSession

from .base import Base


class User(Base, SQLAlchemyBaseUserTable[int]):
    is_admin = Column(Boolean, default=False)

    @classmethod
    def get_db(cls, session: AsyncSession):
        return SQLAlchemyUserDatabase(session, cls)
