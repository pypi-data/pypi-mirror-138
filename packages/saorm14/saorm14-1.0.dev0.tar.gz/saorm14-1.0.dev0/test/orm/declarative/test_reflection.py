from saorm14 import ForeignKey
from saorm14 import Integer
from saorm14 import MetaData
from saorm14 import String
from saorm14 import testing
from saorm14.orm import clear_mappers
from saorm14.orm import decl_api as decl
from saorm14.orm import relationship
from saorm14.testing import assert_raises
from saorm14.testing import eq_
from saorm14.testing import fixtures
from saorm14.testing.fixtures import fixture_session
from saorm14.testing.schema import Column
from saorm14.testing.schema import Table


class DeclarativeReflectionBase(fixtures.TablesTest):
    __requires__ = ("reflectable_autoincrement",)

    def setup_test(self):
        global Base, registry

        registry = decl.registry(metadata=MetaData())
        Base = registry.generate_base()

    def teardown_test(self):
        clear_mappers()


class DeclarativeReflectionTest(DeclarativeReflectionBase):
    @classmethod
    def define_tables(cls, metadata):
        Table(
            "users",
            metadata,
            Column(
                "id", Integer, primary_key=True, test_needs_autoincrement=True
            ),
            Column("name", String(50)),
            test_needs_fk=True,
        )
        Table(
            "addresses",
            metadata,
            Column(
                "id", Integer, primary_key=True, test_needs_autoincrement=True
            ),
            Column("email", String(50)),
            Column("user_id", Integer, ForeignKey("users.id")),
            test_needs_fk=True,
        )
        Table(
            "imhandles",
            metadata,
            Column(
                "id", Integer, primary_key=True, test_needs_autoincrement=True
            ),
            Column("user_id", Integer),
            Column("network", String(50)),
            Column("handle", String(50)),
            test_needs_fk=True,
        )

    def test_basic(self):
        class User(Base, fixtures.ComparableEntity):

            __tablename__ = "users"
            __autoload_with__ = testing.db
            addresses = relationship("Address", backref="user")

        class Address(Base, fixtures.ComparableEntity):

            __tablename__ = "addresses"
            __autoload_with__ = testing.db

        u1 = User(
            name="u1", addresses=[Address(email="one"), Address(email="two")]
        )
        sess = fixture_session()
        sess.add(u1)
        sess.flush()
        sess.expunge_all()
        eq_(
            sess.query(User).all(),
            [
                User(
                    name="u1",
                    addresses=[Address(email="one"), Address(email="two")],
                )
            ],
        )
        a1 = sess.query(Address).filter(Address.email == "two").one()
        eq_(a1, Address(email="two"))
        eq_(a1.user, User(name="u1"))

    def test_rekey_wbase(self):
        class User(Base, fixtures.ComparableEntity):

            __tablename__ = "users"
            __autoload_with__ = testing.db
            nom = Column("name", String(50), key="nom")
            addresses = relationship("Address", backref="user")

        class Address(Base, fixtures.ComparableEntity):

            __tablename__ = "addresses"
            __autoload_with__ = testing.db

        u1 = User(
            nom="u1", addresses=[Address(email="one"), Address(email="two")]
        )
        sess = fixture_session()
        sess.add(u1)
        sess.flush()
        sess.expunge_all()
        eq_(
            sess.query(User).all(),
            [
                User(
                    nom="u1",
                    addresses=[Address(email="one"), Address(email="two")],
                )
            ],
        )
        a1 = sess.query(Address).filter(Address.email == "two").one()
        eq_(a1, Address(email="two"))
        eq_(a1.user, User(nom="u1"))
        assert_raises(TypeError, User, name="u3")

    def test_rekey_wdecorator(self):
        @registry.mapped
        class User(fixtures.ComparableMixin):

            __tablename__ = "users"
            __autoload_with__ = testing.db
            nom = Column("name", String(50), key="nom")
            addresses = relationship("Address", backref="user")

        @registry.mapped
        class Address(fixtures.ComparableMixin):

            __tablename__ = "addresses"
            __autoload_with__ = testing.db

        u1 = User(
            nom="u1", addresses=[Address(email="one"), Address(email="two")]
        )
        sess = fixture_session()
        sess.add(u1)
        sess.flush()
        sess.expunge_all()
        eq_(
            sess.query(User).all(),
            [
                User(
                    nom="u1",
                    addresses=[Address(email="one"), Address(email="two")],
                )
            ],
        )
        a1 = sess.query(Address).filter(Address.email == "two").one()
        eq_(a1, Address(email="two"))
        eq_(a1.user, User(nom="u1"))
        assert_raises(TypeError, User, name="u3")

    def test_supplied_fk(self):
        class IMHandle(Base, fixtures.ComparableEntity):

            __tablename__ = "imhandles"
            __autoload_with__ = testing.db
            user_id = Column("user_id", Integer, ForeignKey("users.id"))

        class User(Base, fixtures.ComparableEntity):

            __tablename__ = "users"
            __autoload_with__ = testing.db
            handles = relationship("IMHandle", backref="user")

        u1 = User(
            name="u1",
            handles=[
                IMHandle(network="blabber", handle="foo"),
                IMHandle(network="lol", handle="zomg"),
            ],
        )
        sess = fixture_session()
        sess.add(u1)
        sess.flush()
        sess.expunge_all()
        eq_(
            sess.query(User).all(),
            [
                User(
                    name="u1",
                    handles=[
                        IMHandle(network="blabber", handle="foo"),
                        IMHandle(network="lol", handle="zomg"),
                    ],
                )
            ],
        )
        a1 = sess.query(IMHandle).filter(IMHandle.handle == "zomg").one()
        eq_(a1, IMHandle(network="lol", handle="zomg"))
        eq_(a1.user, User(name="u1"))
