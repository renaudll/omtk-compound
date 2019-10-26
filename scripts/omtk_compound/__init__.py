"""
Public entry points. All members are part of the public API.
"""
from omtk_compound.core import (
    Compound,
    CompoundDefinition,
    ComponentValidationError,
    Manager,
)

__all__ = ("Compound", "CompoundDefinition", "ComponentValidationError", "manager")

# Default manager
manager = Manager()  # pylint: disable=invalid-name
