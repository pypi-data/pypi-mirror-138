# util/_preloaded.py
# Copyright (C) 2005-2022 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

"""supplies the "preloaded" registry to resolve circular module imports at
runtime.

"""
import sys
from types import ModuleType
import typing
from typing import Any
from typing import Callable
from typing import TypeVar

_FN = TypeVar("_FN", bound=Callable[..., Any])


class _ModuleRegistry:
    """Registry of modules to load in a package init file.

    To avoid potential thread safety issues for imports that are deferred
    in a function, like https://bugs.python.org/issue38884, these modules
    are added to the system module cache by importing them after the packages
    has finished initialization.

    A global instance is provided under the name :attr:`.preloaded`. Use
    the function :func:`.preload_module` to register modules to load and
    :meth:`.import_prefix` to load all the modules that start with the
    given path.

    While the modules are loaded in the global module cache, it's advisable
    to access them using :attr:`.preloaded` to ensure that it was actually
    registered. Each registered module is added to the instance ``__dict__``
    in the form `<package>_<module>`, omitting ``sqlalchemy`` from the package
    name. Example: ``saorm14.sql.util`` becomes ``preloaded.sql_util``.
    """

    def __init__(self, prefix="saorm14."):
        self.module_registry = set()
        self.prefix = prefix

    def preload_module(self, *deps: str) -> Callable[[_FN], _FN]:
        """Adds the specified modules to the list to load.

        This method can be used both as a normal function and as a decorator.
        No change is performed to the decorated object.
        """
        self.module_registry.update(deps)
        return lambda fn: fn

    def import_prefix(self, path: str) -> None:
        """Resolve all the modules in the registry that start with the
        specified path.
        """
        for module in self.module_registry:
            if self.prefix:
                key = module.split(self.prefix)[-1].replace(".", "_")
            else:
                key = module
            if (
                not path or module.startswith(path)
            ) and key not in self.__dict__:
                __import__(module, globals(), locals())
                self.__dict__[key] = sys.modules[module]

    if typing.TYPE_CHECKING:

        def __getattr__(self, key: str) -> ModuleType:
            ...


preloaded = _ModuleRegistry()
preload_module = preloaded.preload_module
