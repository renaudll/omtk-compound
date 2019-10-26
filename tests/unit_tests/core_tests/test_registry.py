"""Test cases for the Registry class."""
import pytest

from omtk_compound.core._definition import CompoundDefinition
from omtk_compound.core._registry import (
    Registry,
    VersionStream,
    AlreadyRegisteredError,
    NotRegisteredError,
)


@pytest.fixture
def registry():
    """Fixture for an empty registry object"""
    return Registry()


@pytest.fixture
def entry1_v1():
    """Fixture for a simple compound v1"""
    return CompoundDefinition(name="testComponent", version="1.0.0", uid=1)


@pytest.fixture
def entry1_v2():
    """Fixture for a simple compound v2"""
    return CompoundDefinition(name="testComponent", version="2.0.0", uid=1)


def test_iter(registry):
    """Validate iterating through an empty registry"""
    assert tuple(registry) == ()


def test_register(registry, entry1_v1):
    """Validate we can register a entry"""
    registry.register(entry1_v1)
    assert tuple(registry) == ((1, "1.0.0"),)


def test_register_invalid(registry):
    """Validate we cannot register an invalid value"""
    with pytest.raises(TypeError) as error:
        registry.register(2)
    assert str(error.value) == "Expected mapping, got int: 2"


def test_register_twice(registry, entry1_v1):
    """Validate an exception is raised if we try to register an entry twice."""
    registry.register(entry1_v1)
    with pytest.raises(AlreadyRegisteredError) as error:
        registry.register(entry1_v1)
    assert str(error.value) == "%s is already registered" % entry1_v1


def test_register_multiple(registry, entry1_v1, entry1_v2):
    """Validate we can register two entities"""
    registry.register(entry1_v1, entry1_v2)
    assert tuple(registry) == ((1, "1.0.0"), (1, "2.0.0"))


def test_unregister(registry, entry1_v1, entry1_v2):
    """Validate we can unregister an entry"""
    registry.register(entry1_v1, entry1_v2)
    registry.unregister(entry1_v1)
    assert tuple(registry) == ((1, "2.0.0"),)


def test_unregister_invalid(registry, entry1_v1):
    """Validate an exception is raised when trying to unregister an invalid entry"""
    with pytest.raises(NotRegisteredError) as error:
        registry.unregister(entry1_v1)
    assert str(error.value) == "%s is not registered" % entry1_v1


def test_get_versions(registry, entry1_v1, entry1_v2):
    """Validate we can access a version stream from a uid"""
    registry.register(entry1_v1, entry1_v2)
    assert type(registry[entry1_v1.uid]) == VersionStream


def test_get_version(registry, entry1_v1, entry1_v2):
    """Validate we can access a version stream from it's version"""
    registry.register(entry1_v1, entry1_v2)
    assert registry[entry1_v1.uid][entry1_v2.version] is entry1_v2


def test_get_version_latest(registry, entry1_v1, entry1_v2):
    """Validate  we can access the latest version of a stream."""
    registry.register(entry1_v1, entry1_v2)
    assert registry[entry1_v1.uid].latest is entry1_v2


# def test_get_latest(registry, entry1_v1, entry1_v2):
#     """Validate we can correctly query the latest version"""
#     registry.register(entry1_v1)
#     registry.register(entry1_v2)
#     assert registry.get_latest(entry1_v1) == entry1_v2
