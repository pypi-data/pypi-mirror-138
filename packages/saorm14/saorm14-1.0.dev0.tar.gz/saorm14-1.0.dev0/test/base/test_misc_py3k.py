import operator
from typing import cast

from saorm14 import Column
from saorm14.testing import eq_
from saorm14.testing import fixtures


class TestGenerics(fixtures.TestBase):
    def test_traversible_is_generic(self):
        """test #6759"""
        col = Column[int]

        # looked in the source for typing._GenericAlias.
        # col.__origin__ is Column, but it's not public API.
        # __reduce__ could change too but seems good enough for now
        eq_(cast(object, col).__reduce__(), (operator.getitem, (Column, int)))
