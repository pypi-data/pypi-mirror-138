from saorm14 import Column
from saorm14 import column
from saorm14 import Integer
from saorm14 import String
from saorm14 import Table
from saorm14 import table
from saorm14 import tablesample
from saorm14.engine import default
from saorm14.sql import func
from saorm14.sql import select
from saorm14.sql import text
from saorm14.sql.selectable import TableSample
from saorm14.testing import assert_raises_message
from saorm14.testing import AssertsCompiledSQL
from saorm14.testing import fixtures


class TableSampleTest(fixtures.TablesTest, AssertsCompiledSQL):
    __dialect__ = default.DefaultDialect(supports_native_boolean=True)

    run_setup_bind = None

    run_create_tables = None

    @classmethod
    def define_tables(cls, metadata):
        Table(
            "people",
            metadata,
            Column("people_id", Integer, primary_key=True),
            Column("age", Integer),
            Column("name", String(30)),
        )

    def test_standalone(self):
        table1 = self.tables.people

        # no special alias handling even though clause is not in the
        # context of a FROM clause
        self.assert_compile(
            tablesample(table1, 1, name="alias"),
            "people AS alias TABLESAMPLE system(:system_1)",
        )

        self.assert_compile(
            table1.tablesample(1, name="alias"),
            "people AS alias TABLESAMPLE system(:system_1)",
        )

        self.assert_compile(
            tablesample(
                table1, func.bernoulli(1), name="alias", seed=func.random()
            ),
            "people AS alias TABLESAMPLE bernoulli(:bernoulli_1) "
            "REPEATABLE (random())",
        )

    def test_select_from(self):
        table1 = self.tables.people

        self.assert_compile(
            select(table1.tablesample(text("1"), name="alias").c.people_id),
            "SELECT alias.people_id FROM "
            "people AS alias TABLESAMPLE system(1)",
        )

    def test_no_alias_construct(self):
        a = table("a", column("x"))

        assert_raises_message(
            NotImplementedError,
            "The TableSample class is not intended to be constructed "
            "directly.  "
            r"Please use the tablesample\(\) standalone",
            TableSample,
            a,
            "foo",
        )
