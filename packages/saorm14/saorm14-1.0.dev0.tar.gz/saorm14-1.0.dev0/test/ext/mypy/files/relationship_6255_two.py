from typing import List
from typing import Optional

from saorm14 import Column
from saorm14 import ForeignKey
from saorm14 import Integer
from saorm14 import select
from saorm14 import String
from saorm14.orm import declarative_base
from saorm14.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    addresses: List["Address"] = relationship("Address", back_populates="user")

    @property
    def some_property(self) -> List[Optional[int]]:
        return [i.id for i in self.addresses]


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    user_id: int = Column(ForeignKey("user.id"))

    user: "User" = relationship("User", back_populates="addresses")

    @property
    def some_other_property(self) -> Optional[str]:
        return self.user.name


# it's in the constructor, correct type
u1 = User(addresses=[Address()])

# knows it's an iterable
[x for x in u1.addresses]

# knows it's Mapped
stmt = select(User).where(User.addresses.any(id=5))
