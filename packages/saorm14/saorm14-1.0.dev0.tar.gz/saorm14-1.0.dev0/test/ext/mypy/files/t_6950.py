from typing import cast

from saorm14 import Column
from saorm14 import Integer
from saorm14.orm import declarative_base
from saorm14.orm import Mapped
from saorm14.orm import query_expression
from saorm14.orm import Session
from saorm14.orm import with_expression

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    foo = Column(Integer)

    question_count: Mapped[int] = query_expression()
    answer_count: int = query_expression()


s = Session()

q = s.query(User).options(with_expression(User.question_count, User.foo + 5))

u1: User = cast(User, q.first())

qc: int = u1.question_count
print(qc)
