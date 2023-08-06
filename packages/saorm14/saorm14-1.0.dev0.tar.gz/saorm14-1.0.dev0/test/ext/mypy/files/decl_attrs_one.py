from saorm14 import Column
from saorm14 import Integer
from saorm14 import String
from saorm14.orm import registry
from saorm14.sql.schema import ForeignKey
from saorm14.sql.schema import MetaData
from saorm14.sql.schema import Table


reg: registry = registry()


@reg.mapped
class Foo:
    __tablename__ = "foo"
    id: int = Column(Integer(), primary_key=True)
    name: str = Column(String)


@reg.mapped
class Bar(Foo):
    __tablename__ = "bar"
    id: int = Column(ForeignKey("foo.id"), primary_key=True)


@reg.mapped
class Bat(Foo):
    pass


m1: MetaData = reg.metadata

t1: Table = Foo.__table__

t2: Table = Bar.__table__

t3: Table = Bat.__table__
