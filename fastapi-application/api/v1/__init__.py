from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from core.config import settings
from .auth import router as auth_router
from .users import router as user_router
from .accounts import router as account_router
from .invoices import router as invoice_router


http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(
    prefix=settings.api.v1.prefix,
    dependencies=[Depends(http_bearer)],
)

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(account_router)
router.include_router(invoice_router)
