"""
Highest logical level for compound manipulation.
"""

import os
import logging
from typing import Any

from ._constants import COMPOUND_DEFAULT_NAMESPACE
from ._definition import CompoundDefinition
from ._factory import from_file
from ._registry import Registry
from ._preferences import Preferences

_LOG = logging.getLogger(__name__)


class Manager:
    """
    Main point of entry for interaction with the scene, registry and preferences.
    """

    def __init__(
        self, registry: Registry | None = None, preferences: Preferences | None = None
    ) -> None:
        self.registry = registry or Registry()
        self.preferences = preferences or Preferences()

        self.registry.parse_directory(self.preferences.compound_location)

    def create_compound(
        self,
        uid: Any = None,
        name: Any = None,
        version: Any = None,
        namespace: str = COMPOUND_DEFAULT_NAMESPACE,
    ) -> Any:
        """
        :raises ValueError:
        :raises LookupError: If no compound could be found.
        """
        compound_def = self.registry.find(uid=uid, name=name, version=version)
        return from_file(compound_def.path, namespace=namespace)

    def publish_compound(self, compound: Any, force: bool = False) -> None:
        """Publish a compound

        :param compound: The compound to publish
        :param force: Should we overwrite if the destination file exist?
        """
        compound_def = CompoundDefinition(**compound.get_metadata())
        path = self._get_publish_location(compound_def)

        compound_def["path"] = path

        if os.path.exists(path) and not force:
            raise ValueError(f"Compound path already exist on disk. {path!r}")

        compound.export(path)
        self.registry.register(compound_def)

    def update_compound(self, compound: Any, version: Any = None) -> None:
        """Update a compound to a new version.

        :param compound:
        :param version: An optional version string. Otherwise the highest is used.
        """
        metadata = compound.get_metadata()
        stream = self.registry[metadata["uid"]]
        compound_def = stream[version] if version else stream.latest
        path = compound_def["path"]

        namespace = compound.namespace
        old_compound = compound
        new_compound = from_file(path)
        connections = old_compound.hold_connections()
        new_compound.fetch_connections(*connections)
        old_compound.delete()
        new_compound.rename(namespace)

    def _get_publish_location(self, compound_def: CompoundDefinition) -> str:
        """Resolve the destination path of a compound we want to publish.

        :param compound_def: A compound definition
        :return: A destination path
        """
        return os.path.join(
            self.preferences.compound_location,
            f"{compound_def.name}_v{compound_def.version}.ma",
        )
