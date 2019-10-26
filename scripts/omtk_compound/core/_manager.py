"""
Highest logical level for compound manipulation.
"""
import os
import logging

from omtk_compound.core._definition import CompoundDefinition
from omtk_compound.core._factory import from_file
from omtk_compound.core._registry import Registry
from omtk_compound.core._preferences import Preferences

_LOG = logging.getLogger(__name__)


class Manager(object):
    """
    Main point of entry for interaction with the scene, registry and preferences.
    """
    def __init__(self, registry=None, preferences=None):
        self.registry = registry or Registry()
        self.preferences = preferences or Preferences()

        self.registry.parse_directory(self.preferences.compound_location)

    def _get_publish_location(self, compound_def):
        """ Resolve the destination path of a compound we want to publish.

        :param CompoundDefinition compound_def: A compound definition
        :return: A destination path
        :rtype: str
        """
        return os.path.join(
            self.preferences.compound_location,
            "%s_v%s.ma" % (compound_def.name, compound_def.version),
        )

    def publish_compound(self, compound, force=False):
        """ Publish a compound

        :param Component compound: The compound to publish
        :param bool force: Should we overwrite the file if the compound is already published?
        """
        compound_def = CompoundDefinition(**compound.get_metadata())
        path = self._get_publish_location(compound_def)

        compound_def["path"] = path

        if os.path.exists(path) and not force:
            raise ValueError("Component path already exist on disk. %r" % path)

        compound.export(path)
        self.registry.register(compound_def)

    def update_compound(self, compound, version=None):
        """ Update a compound to a new version.

        :param Component compound:
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
