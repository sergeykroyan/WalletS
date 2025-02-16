from fastapi import APIRouter

from api.schemas.users import UserRead, UserUpdate
from api.v1.fastapi_users import fastapi_users
from core.config import settings

router = APIRouter(prefix=settings.api.v1.users, tags=["Users"])

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
)
