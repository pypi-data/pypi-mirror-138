from saorm14 import Column
from saorm14 import Integer
from saorm14 import String
from saorm14.orm import registry

reg: registry = registry()


@reg.mapped
class Foo:
    pass
    id: int = Column(Integer())
    name: str = Column(String)


f1 = Foo()


# EXPECTED_MYPY: Name 'u1' is not defined
p: str = u1.name  # noqa
