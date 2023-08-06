from typing import Set

from saorm14 import Column
from saorm14 import ForeignKey
from saorm14 import Integer
from saorm14 import String
from saorm14.ext.declarative import declarative_base
from saorm14.orm import relationship

Base = declarative_base()


class B(Base):
    __tablename__ = "b"
    id = Column(Integer, primary_key=True)
    a_id: int = Column(ForeignKey("a.id"))
    data = Column(String)


class A(Base):
    __tablename__ = "a"

    id = Column(Integer, primary_key=True)
    data = Column(String)
    bs = relationship(B, uselist=True)


# EXPECTED_MYPY: List item 1 has incompatible type "A"; expected "B"
a1 = A(bs=[B(data="b"), A()])

# EXPECTED_MYPY: Incompatible types in assignment (expression has type "List[B]", variable has type "Set[B]") # noqa
x: Set[B] = a1.bs
