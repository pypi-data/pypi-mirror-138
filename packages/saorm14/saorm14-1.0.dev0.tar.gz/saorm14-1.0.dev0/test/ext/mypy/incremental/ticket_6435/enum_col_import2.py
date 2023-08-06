from saorm14 import Column
from saorm14 import Enum
from saorm14.orm import declarative_base
from saorm14.orm import Mapped
from . import enum_col_import1
from .enum_col_import1 import IntEnum
from .enum_col_import1 import StrEnum

Base = declarative_base()


class TestEnum(Base):
    __tablename__ = "test_enum"

    e1: Mapped[StrEnum] = Column(Enum(StrEnum))
    e2: StrEnum = Column(Enum(StrEnum))

    e3: Mapped[IntEnum] = Column(Enum(IntEnum))
    e4: IntEnum = Column(Enum(IntEnum))

    e5: Mapped[enum_col_import1.StrEnum] = Column(
        Enum(enum_col_import1.StrEnum)
    )
    e6: enum_col_import1.StrEnum = Column(Enum(enum_col_import1.StrEnum))

    e7: Mapped[enum_col_import1.IntEnum] = Column(
        Enum(enum_col_import1.IntEnum)
    )
    e8: enum_col_import1.IntEnum = Column(Enum(enum_col_import1.IntEnum))
