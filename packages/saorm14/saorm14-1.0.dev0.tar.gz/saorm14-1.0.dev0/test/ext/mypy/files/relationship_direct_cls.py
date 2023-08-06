from typing import List
from typing import Optional

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

    a: Optional["A"] = relationship("A", back_populates="bs")


class A(Base):
    __tablename__ = "a"

    id = Column(Integer, primary_key=True)
    data = Column(String)
    bs = relationship(B, uselist=True, back_populates="a")


a1 = A(bs=[B(data="b"), B(data="b")])

x: List[B] = a1.bs


b1 = B(a=A())
