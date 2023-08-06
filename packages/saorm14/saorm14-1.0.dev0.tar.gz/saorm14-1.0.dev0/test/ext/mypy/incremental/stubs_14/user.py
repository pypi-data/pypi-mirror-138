from typing import List
from typing import TYPE_CHECKING

from saorm14 import Column
from saorm14 import ForeignKey
from saorm14 import Integer
from saorm14 import String
from saorm14.orm import Mapped
from saorm14.orm import relationship
from saorm14.orm.decl_api import declared_attr
from saorm14.orm.relationships import RelationshipProperty
from . import Base

if TYPE_CHECKING:
    from .address import Address


class User(Base):
    name = Column(String)

    othername = Column(String)

    addresses: Mapped[List["Address"]] = relationship(
        "Address", back_populates="user"
    )


class HasUser:
    @declared_attr
    def user_id(self) -> "Column[Integer]":
        return Column(
            Integer,
            ForeignKey(User.id, ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False,
        )

    @declared_attr
    def user(self) -> RelationshipProperty[User]:
        return relationship(User)
