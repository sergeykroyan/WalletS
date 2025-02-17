from fastapi_users import FastAPIUsers

from api.dependencies.auth.user_manager import get_user_manager
from api.dependencies.auth.backend import auth_backend
from core.models import User


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
