from saorm14 import Column
from saorm14 import Integer
from saorm14 import String
from saorm14.orm import registry

reg: registry = registry()


@reg.as_declarative_base()
class Base:
    updated_at = Column(Integer)


class Foo(Base):
    __tablename__ = "foo"
    id: int = Column(Integer(), primary_key=True)
    name: str = Column(String)


f1 = Foo()

val: int = f1.id

p: str = f1.name

Foo.id.property

f2 = Foo(name="some name", updated_at=5)
