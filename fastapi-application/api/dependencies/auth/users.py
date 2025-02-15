from typing import TYPE_CHECKING
from fastapi import Depends
from core.models import User
from core.models.db_helper import DBHelper

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_db(session: "AsyncSession" = Depends(DBHelper.session_getter)):
    yield User.get_db(session=session)
