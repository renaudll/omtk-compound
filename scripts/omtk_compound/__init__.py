"""
Public entry points. All members are part of the public API.
"""
from omtk_compound.core import (
    Compound,
    CompoundDefinition,
    ComponentValidationError,
    Manager,
    Registry,
)

__all__ = ("Compound", "CompoundDefinition", "ComponentValidationError", "Registry", "manager")

# Default manager
manager = Manager()  # pylint: disable=invalid-name
