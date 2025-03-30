"""
Registry hold all known compound definitions.
"""

import os
from collections.abc import Mapping
from collections import defaultdict
from typing import Iterator, Tuple

from ._definition import CompoundDefinition


class RegistryError(Exception):
    """Base class for registry errors"""


class AlreadyRegisteredError(RegistryError):
    """Exception raised when trying to register an already registered entry."""


class NotRegisteredError(RegistryError):
    """Exception raised when trying to unregister an entry that was not registered."""


class VersionStream(dict):
    """Extended dict."""

    def __setitem__(self, key, value) -> None:
        if key in self:
            raise AlreadyRegisteredError(f"{value} is already registered")
        super().__setitem__(key, value)

    @property
    def latest(self) -> CompoundDefinition:
        """:return: The highest version available"""
        key = sorted(self.keys())[-1]
        return self[key]


class Registry:
    """A registry of compounds definitions."""

    def __init__(self) -> None:
        self._store = defaultdict(VersionStream)

    def __iter__(self) -> Iterator[Tuple[str, CompoundDefinition]]:
        for uid, versions in self._store.items():
            for version in versions:
                yield uid, version

    def __len__(self) -> int:
        return len(tuple(iter(self)))

    def __getitem__(self, item: str) -> VersionStream:
        return self._store[item]

    def __eq__(self, other) -> bool:
        return tuple(self) == tuple(other)

    def find(
        self, uid: str = None, name: str = None, version: int = None
    ) -> CompoundDefinition:
        """
        Find a single compound definition.

        :param uid: Optional compound uid to search for.
        :param name: Optional compound name to search for.
        :param version: Optional compound version to search for. Default is latest.
        :raises ValueError: If the requirements are invalid.
        :raises LookupError: If no compound definition is found.
        """
        if not any((name, uid)):
            raise ValueError("Should at least have one query.")

        for stream in self._store.values():
            compound = stream.get(version) if version else stream.latest
            if compound and (
                (uid and compound.uid == uid) or (name and compound.name == name)
            ):
                return compound

        raise LookupError("Found no compound matching requirements.")

    def register(self, *entries: Mapping) -> None:
        """
        Register entries

        :param entries: The entries to register
        :raises TypeError: If the provided value is not a valid mapping
        :raises AlreadyRegisteredError: If the provided entry is already registered
        """
        for entry in entries:
            if not isinstance(entry, Mapping):
                raise TypeError(
                    f"Expected mapping, got {type(entry).__name__}: {entry}"
                )

            self._store[entry.uid][entry.version] = entry

    def unregister(self, entry: CompoundDefinition) -> None:
        """Unregister an entry

        :param entry: The entry to unregister
        :raises NotRegisteredError: When the entry to unregister was never registered.
        """
        try:
            self._store[entry.uid].pop(entry.version)
        except KeyError:
            raise NotRegisteredError(f"{entry} is not registered")

    def parse_directory(self, startdir: str) -> None:
        """Scan a directory and register any found definitions."""
        for rootdir, _, filenames in os.walk(startdir):
            for filename in filenames:
                if filename.endswith(".ma"):
                    path = os.path.join(rootdir, filename)
                    try:
                        inst = CompoundDefinition.from_file(path)
                    except ValueError:  # TODO: Use custom exception
                        pass
                    else:
                        self.register(inst)
