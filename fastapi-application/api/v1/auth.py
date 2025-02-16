from fastapi import APIRouter

from api.dependencies.auth.backend import auth_backend
from api.schemas.users import UserRead, UserCreate
from api.v1.fastapi_users import fastapi_users
from core.config import settings

router = APIRouter(prefix=settings.api.v1.auth, tags=["Auth"])

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
)

router.include_router(
    fastapi_users.get_register_router(
        UserRead,
        UserCreate,
    )
)
