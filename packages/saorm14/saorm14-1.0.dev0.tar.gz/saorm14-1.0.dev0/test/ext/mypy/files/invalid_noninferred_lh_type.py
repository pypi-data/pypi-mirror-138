from saorm14 import Column
from saorm14 import Integer
from saorm14 import String
from saorm14.orm import registry

reg: registry = registry()


@reg.mapped
class User:
    __tablename__ = "user"

    id = Column(Integer(), primary_key=True)
    # EXPECTED: Left hand assignment 'name: "int"' not compatible with ORM mapped expression # noqa E501
    name: int = Column(String())
