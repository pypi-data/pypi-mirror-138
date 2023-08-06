# orm/properties.py
# Copyright (C) 2005-2022 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

"""MapperProperty implementations.

This is a private module which defines the behavior of individual ORM-
mapped attributes.

"""

from typing import Any
from typing import TypeVar

from . import attributes
from . import strategy_options
from .descriptor_props import CompositeProperty
from .descriptor_props import ConcreteInheritedProperty
from .descriptor_props import SynonymProperty
from .interfaces import PropComparator
from .interfaces import StrategizedProperty
from .relationships import RelationshipProperty
from .util import _orm_full_deannotate
from .. import log
from .. import sql
from .. import util
from ..sql import coercions
from ..sql import roles

_T = TypeVar("_T", bound=Any)
_PT = TypeVar("_PT", bound=Any)

__all__ = [
    "ColumnProperty",
    "CompositeProperty",
    "ConcreteInheritedProperty",
    "RelationshipProperty",
    "SynonymProperty",
]


@log.class_logger
class ColumnProperty(StrategizedProperty[_T]):
    """Describes an object attribute that corresponds to a table column.

    Public constructor is the :func:`_orm.column_property` function.

    """

    strategy_wildcard_key = strategy_options._COLUMN_TOKEN
    inherit_cache = True
    _links_to_entity = False

    __slots__ = (
        "_orig_columns",
        "columns",
        "group",
        "deferred",
        "instrument",
        "comparator_factory",
        "descriptor",
        "active_history",
        "expire_on_flush",
        "doc",
        "strategy_key",
        "_creation_order",
        "_is_polymorphic_discriminator",
        "_mapped_by_synonym",
        "_deferred_column_loader",
        "_raise_column_loader",
        "_renders_in_subqueries",
        "raiseload",
    )

    def __init__(
        self, column: sql.ColumnElement[_T], *additional_columns, **kwargs
    ):
        super(ColumnProperty, self).__init__()
        columns = (column,) + additional_columns
        self._orig_columns = [
            coercions.expect(roles.LabeledColumnExprRole, c) for c in columns
        ]
        self.columns = [
            coercions.expect(
                roles.LabeledColumnExprRole, _orm_full_deannotate(c)
            )
            for c in columns
        ]
        self.parent = self.key = None
        self.group = kwargs.pop("group", None)
        self.deferred = kwargs.pop("deferred", False)
        self.raiseload = kwargs.pop("raiseload", False)
        self.instrument = kwargs.pop("_instrument", True)
        self.comparator_factory = kwargs.pop(
            "comparator_factory", self.__class__.Comparator
        )
        self.descriptor = kwargs.pop("descriptor", None)
        self.active_history = kwargs.pop("active_history", False)
        self.expire_on_flush = kwargs.pop("expire_on_flush", True)

        if "info" in kwargs:
            self.info = kwargs.pop("info")

        if "doc" in kwargs:
            self.doc = kwargs.pop("doc")
        else:
            for col in reversed(self.columns):
                doc = getattr(col, "doc", None)
                if doc is not None:
                    self.doc = doc
                    break
            else:
                self.doc = None

        if kwargs:
            raise TypeError(
                "%s received unexpected keyword argument(s): %s"
                % (self.__class__.__name__, ", ".join(sorted(kwargs.keys())))
            )

        util.set_creation_order(self)

        self.strategy_key = (
            ("deferred", self.deferred),
            ("instrument", self.instrument),
        )
        if self.raiseload:
            self.strategy_key += (("raiseload", True),)

    def _memoized_attr__renders_in_subqueries(self):
        return ("deferred", True) not in self.strategy_key or (
            self not in self.parent._readonly_props
        )

    @util.preload_module("saorm14.orm.state", "saorm14.orm.strategies")
    def _memoized_attr__deferred_column_loader(self):
        state = util.preloaded.orm_state
        strategies = util.preloaded.orm_strategies
        return state.InstanceState._instance_level_callable_processor(
            self.parent.class_manager,
            strategies.LoadDeferredColumns(self.key),
            self.key,
        )

    @util.preload_module("saorm14.orm.state", "saorm14.orm.strategies")
    def _memoized_attr__raise_column_loader(self):
        state = util.preloaded.orm_state
        strategies = util.preloaded.orm_strategies
        return state.InstanceState._instance_level_callable_processor(
            self.parent.class_manager,
            strategies.LoadDeferredColumns(self.key, True),
            self.key,
        )

    def __clause_element__(self):
        """Allow the ColumnProperty to work in expression before it is turned
        into an instrumented attribute.
        """

        return self.expression

    @property
    def expression(self):
        """Return the primary column or expression for this ColumnProperty.

        E.g.::


            class File(Base):
                # ...

                name = Column(String(64))
                extension = Column(String(8))
                filename = column_property(name + '.' + extension)
                path = column_property('C:/' + filename.expression)

        .. seealso::

            :ref:`mapper_column_property_sql_expressions_composed`

        """
        return self.columns[0]

    def instrument_class(self, mapper):
        if not self.instrument:
            return

        attributes.register_descriptor(
            mapper.class_,
            self.key,
            comparator=self.comparator_factory(self, mapper),
            parententity=mapper,
            doc=self.doc,
        )

    def do_init(self):
        super(ColumnProperty, self).do_init()

        if len(self.columns) > 1 and set(self.parent.primary_key).issuperset(
            self.columns
        ):
            util.warn(
                (
                    "On mapper %s, primary key column '%s' is being combined "
                    "with distinct primary key column '%s' in attribute '%s'. "
                    "Use explicit properties to give each column its own "
                    "mapped attribute name."
                )
                % (self.parent, self.columns[1], self.columns[0], self.key)
            )

    def copy(self):
        return ColumnProperty(
            deferred=self.deferred,
            group=self.group,
            active_history=self.active_history,
            *self.columns,
        )

    def _getcommitted(
        self, state, dict_, column, passive=attributes.PASSIVE_OFF
    ):
        return state.get_impl(self.key).get_committed_value(
            state, dict_, passive=passive
        )

    def merge(
        self,
        session,
        source_state,
        source_dict,
        dest_state,
        dest_dict,
        load,
        _recursive,
        _resolve_conflict_map,
    ):
        if not self.instrument:
            return
        elif self.key in source_dict:
            value = source_dict[self.key]

            if not load:
                dest_dict[self.key] = value
            else:
                impl = dest_state.get_impl(self.key)
                impl.set(dest_state, dest_dict, value, None)
        elif dest_state.has_identity and self.key not in dest_dict:
            dest_state._expire_attributes(
                dest_dict, [self.key], no_loader=True
            )

    class Comparator(util.MemoizedSlots, PropComparator[_PT]):
        """Produce boolean, comparison, and other operators for
        :class:`.ColumnProperty` attributes.

        See the documentation for :class:`.PropComparator` for a brief
        overview.

        .. seealso::

            :class:`.PropComparator`

            :class:`.ColumnOperators`

            :ref:`types_operators`

            :attr:`.TypeEngine.comparator_factory`

        """

        __slots__ = "__clause_element__", "info", "expressions"

        def _orm_annotate_column(self, column):
            """annotate and possibly adapt a column to be returned
            as the mapped-attribute exposed version of the column.

            The column in this context needs to act as much like the
            column in an ORM mapped context as possible, so includes
            annotations to give hints to various ORM functions as to
            the source entity of this column.   It also adapts it
            to the mapper's with_polymorphic selectable if one is
            present.

            """

            pe = self._parententity
            annotations = {
                "entity_namespace": pe,
                "parententity": pe,
                "parentmapper": pe,
                "proxy_key": self.prop.key,
            }

            col = column

            # for a mapper with polymorphic_on and an adapter, return
            # the column against the polymorphic selectable.
            # see also orm.util._orm_downgrade_polymorphic_columns
            # for the reverse operation.
            if self._parentmapper._polymorphic_adapter:
                mapper_local_col = col
                col = self._parentmapper._polymorphic_adapter.traverse(col)

                # this is a clue to the ORM Query etc. that this column
                # was adapted to the mapper's polymorphic_adapter.  the
                # ORM uses this hint to know which column its adapting.
                annotations["adapt_column"] = mapper_local_col

            return col._annotate(annotations)._set_propagate_attrs(
                {"compile_state_plugin": "orm", "plugin_subject": pe}
            )

        def _memoized_method___clause_element__(self):
            if self.adapter:
                return self.adapter(self.prop.columns[0], self.prop.key)
            else:
                return self._orm_annotate_column(self.prop.columns[0])

        def _memoized_attr_info(self):
            """The .info dictionary for this attribute."""

            ce = self.__clause_element__()
            try:
                return ce.info
            except AttributeError:
                return self.prop.info

        def _memoized_attr_expressions(self):
            """The full sequence of columns referenced by this
            attribute, adjusted for any aliasing in progress.

            .. versionadded:: 1.3.17

            """
            if self.adapter:
                return [
                    self.adapter(col, self.prop.key)
                    for col in self.prop.columns
                ]
            else:
                return [
                    self._orm_annotate_column(col) for col in self.prop.columns
                ]

        def _fallback_getattr(self, key):
            """proxy attribute access down to the mapped column.

            this allows user-defined comparison methods to be accessed.
            """
            return getattr(self.__clause_element__(), key)

        def operate(self, op, *other, **kwargs):
            return op(self.__clause_element__(), *other, **kwargs)

        def reverse_operate(self, op, other, **kwargs):
            col = self.__clause_element__()
            return op(col._bind_param(op, other), col, **kwargs)

    def __str__(self):
        if not self.parent or not self.key:
            return object.__repr__(self)
        return str(self.parent.class_.__name__) + "." + self.key
