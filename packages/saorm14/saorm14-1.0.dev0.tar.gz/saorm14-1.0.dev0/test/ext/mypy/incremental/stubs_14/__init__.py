from typing import TYPE_CHECKING

from saorm14 import Column
from saorm14 import Integer
from saorm14.orm import as_declarative
from saorm14.orm import declared_attr
from saorm14.orm import Mapped
from .address import Address
from .user import User

if TYPE_CHECKING:
    from saorm14.orm.decl_api import DeclarativeMeta


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(self) -> Mapped[str]:
        return self.__name__.lower()

    id = Column(Integer, primary_key=True)


__all__ = ["User", "Address"]
