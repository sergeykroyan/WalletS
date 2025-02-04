from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base


class User(Base):
    username: Mapped[str] = mapped_column(unique=True)

    @property
    def email(self) -> str:
        return f"{self.username}@gmail.com"
