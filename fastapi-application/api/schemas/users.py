from fastapi_users import schemas
from pydantic import Field
from typing import Optional


class UserRead(schemas.BaseUser[int]):
    id: int
    is_admin: bool


class UserCreate(schemas.BaseUserCreate):
    is_admin: bool = Field(default=False)


class UserUpdate(schemas.BaseUserUpdate):
    is_admin: Optional[bool] = None
