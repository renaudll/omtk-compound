"""
A CompoundDefinition holds information about a registered compound.
"""

import logging
import uuid

from ._parser import write_metadata_to_ma_file, get_metadata_from_file
from ..vendor.packaging import version

_LOG = logging.getLogger(__name__)

_MANDATORY_FIELDS = {"uid", "name", "version"}


def _validate(mapping: dict[str, str]) -> None:
    """Ensure all mandatory keys in a definition mapping are defined.

    :param mapping: A definition dict
    :raises ValueError: If some mandatory keys are missing
    """
    missing_fields = _MANDATORY_FIELDS - set(mapping)
    if missing_fields:
        raise ValueError(
            f"Missing mandatory fields: {', '.join(repr(field) for field in sorted(missing_fields))}"
        )


class CompoundDefinition(dict):
    """
    A CompoundDefinition holds information about a compound registered on disk.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        :raises ValueError: If some mandatory fields were not provided.
        """
        super().__init__(*args, **kwargs)

        self["uid"] = self.get("uid", None) or str(uuid.uuid4())
        self["name"] = self.get("name") or "unamed"
        self["version"] = self.get("version") or "0.0.0"
        self["description"] = self.get("description") or ""

        _validate(self)

    def __repr__(self) -> str:
        return f"<CompoundDefinition {self.name} v{self.version}>"

    def __eq__(self, other) -> bool:
        return self.name == other.name and self.version == other.version

    def __ne__(self, other) -> bool:
        return not self == other

    def __gt__(self, other) -> bool:
        return self.name > other.name or (
            self.name == other.name
            and version.parse(self.version) > version.parse(other.version)
        )

    def __lt__(self, other) -> bool:
        return self.name < other.name or (
            self.name == other.name
            and version.parse(self.version) < version.parse(other.version)
        )

    def __ge__(self, other) -> bool:
        return self == other or self > other

    def __le__(self, other) -> bool:
        return self == other or self < other

    # Helper properties
    @property
    def uid(self) -> str:
        """
        :return: The compound unique identifier
        """
        return self["uid"]

    @property
    def name(self) -> str:
        """
        :return: The compound name
        """
        return self["name"]

    @property
    def version(self) -> str:
        """
        :return: The compound semantic formatted version
        """
        return self["version"]

    @property
    def author(self) -> str | None:
        """
        :return: The compound author
        """
        return self.get("author", None)

    @property
    def path(self) -> str:
        """
        :return: The compound path on disk
        """
        return self["path"]

    @property
    def description(self) -> str:
        """
        :return: The compound description provided by the author
        """
        return self["description"]

    # Class constructors

    @classmethod
    def from_file(cls, path: str) -> "CompoundDefinition":
        """Initialize a compound definition from a maya file by parsing its header.

        :param path:
        :return: A new compound definition instance
        """
        metadata = get_metadata_from_file(path)
        metadata["path"] = path
        _validate(metadata)
        return cls(**metadata)

    def write_metadata_to_file(self, path: str) -> bool:
        """Write the definition to a maya ascii (.ma) file.

        :param path: Path to a maya ascii (.ma) file
        :return: True if successful, False otherwise.
        """
        return write_metadata_to_ma_file(path, self)
