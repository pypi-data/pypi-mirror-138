"""
test inspect()

however this is not really working

"""
from saorm14 import Column
from saorm14 import create_engine
from saorm14 import inspect
from saorm14 import Integer
from saorm14 import String
from saorm14.engine.reflection import Inspector
from saorm14.ext.declarative import declarative_base
from saorm14.orm import Mapper

Base = declarative_base()


class A(Base):
    __tablename__ = "a"

    id = Column(Integer, primary_key=True)
    data = Column(String)


a1 = A(data="d")

e = create_engine("sqlite://")

# TODO: I can't get these to work, pylance and mypy both don't want
# to accommodate for different types for the first argument

t: bool = inspect(a1).transient

m: Mapper = inspect(A)

inspect(e).get_table_names()

i: Inspector = inspect(e)


with e.connect() as conn:
    inspect(conn).get_table_names()
