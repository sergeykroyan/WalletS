from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Boolean

from .base import Base


class User(Base, SQLAlchemyBaseUserTable[int]):
    is_admin = Column(Boolean, default=False)
