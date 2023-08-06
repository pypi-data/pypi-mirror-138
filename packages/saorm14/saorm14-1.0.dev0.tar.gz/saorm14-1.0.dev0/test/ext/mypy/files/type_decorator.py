from typing import Any
from typing import Optional

from saorm14 import Column
from saorm14 import Integer
from saorm14 import String
from saorm14 import TypeDecorator
from saorm14.ext.declarative import declarative_base

Base = declarative_base()


class IntToStr(TypeDecorator[int]):
    impl = String
    cache_ok = True

    def process_bind_param(
        self,
        value: Any,
        dialect: Any,
    ) -> Optional[str]:
        return str(value) if value is not None else value

    def process_result_value(
        self,
        value: Any,
        dialect: Any,
    ) -> Optional[int]:
        return int(value) if value is not None else value

    def copy(self, **kwargs: Any) -> "IntToStr":
        return IntToStr(self.impl.length)


class Thing(Base):
    __tablename__ = "things"

    id: int = Column(Integer, primary_key=True)
    intToStr: int = Column(IntToStr)


t1 = Thing(intToStr=5)

i5: int = t1.intToStr

t1.intToStr = 8
