"""
Private package holding the core logic.
Do not use from outside.
"""
from ._compound import Compound, ComponentValidationError
from ._definition import CompoundDefinition
from ._factory import create_empty, create_from_nodes, from_attributes, from_namespace
from ._registry import Registry
from ._preferences import Preferences
from ._manager import Manager

__all__ = (
    "Compound",
    "ComponentValidationError",
    "CompoundDefinition",
    "create_empty",
    "create_from_nodes",
    "from_attributes",
    "from_namespace",
    "Registry",
    "Preferences",
    "Manager",
)
