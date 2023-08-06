from typing import Callable

from saorm14 import Column
from saorm14 import Integer
from saorm14 import String
from saorm14.orm import deferred
from saorm14.orm import Mapped
from saorm14.orm.decl_api import declarative_mixin
from saorm14.orm.decl_api import declared_attr
from saorm14.orm.interfaces import MapperProperty


def some_other_decorator(fn: Callable[..., None]) -> Callable[..., None]:
    return fn


@declarative_mixin
class HasAMixin:
    x: Mapped[int] = Column(Integer)

    y = Column(String)

    @declared_attr
    def data(cls) -> Column[String]:
        return Column(String)

    @declared_attr
    def data2(cls) -> MapperProperty[str]:
        return deferred(Column(String))

    @some_other_decorator
    def q(cls) -> None:
        return None
