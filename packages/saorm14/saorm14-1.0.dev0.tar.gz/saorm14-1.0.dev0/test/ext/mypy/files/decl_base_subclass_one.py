from saorm14 import Column
from saorm14 import Integer
from saorm14 import String
from saorm14.orm import declarative_base


class _Base:
    updated_at = Column(Integer)


Base = declarative_base(cls=_Base)


class Foo(Base):
    __tablename__ = "foo"
    id: int = Column(Integer(), primary_key=True)
    name: str = Column(String)


class Bar(Base):
    __tablename__ = "bar"
    id = Column(Integer(), primary_key=True)
    num = Column(Integer)


Foo.updated_at.in_([1, 2, 3])

f1 = Foo(name="name", updated_at=5)

b1 = Bar(num=5, updated_at=6)
