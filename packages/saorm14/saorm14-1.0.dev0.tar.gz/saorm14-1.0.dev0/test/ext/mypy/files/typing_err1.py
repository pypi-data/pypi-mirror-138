from saorm14 import Column
from saorm14 import Integer
from saorm14.orm import registry
from saorm14.types import TypeEngine


# EXPECTED_MYPY: Missing type parameters for generic type "TypeEngine"
class MyCustomType(TypeEngine):
    pass


# correct way
class MyOtherCustomType(TypeEngine[str]):
    pass


reg: registry = registry()


@reg.mapped
class Foo:
    id: int = Column(Integer())

    name = Column(MyCustomType())
    other_name: str = Column(MyCustomType())

    name2 = Column(MyOtherCustomType())
    other_name2: str = Column(MyOtherCustomType())


Foo(name="x", other_name="x", name2="x", other_name2="x")
