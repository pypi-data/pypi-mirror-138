from typing import TYPE_CHECKING

from . import Base
from .user import HasUser

if TYPE_CHECKING:
    from saorm14 import Column  # noqa
    from saorm14 import Integer  # noqa
    from saorm14.orm import RelationshipProperty  # noqa
    from .user import User  # noqa


class Address(Base, HasUser):
    pass
