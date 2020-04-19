"""Test cases for the Registry class."""
# pylint: disable=redefined-outer-name
import pytest

from omtk_compound.core._definition import CompoundDefinition
from omtk_compound.core._registry import (
    Registry,
    VersionStream,
    AlreadyRegisteredError,
    NotRegisteredError,
)


@pytest.fixture
def registry_empty():
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


@pytest.fixture
def registry(entry1_v1, entry1_v2):
    """Fixture for a non-empty registry."""
    registry = Registry()
    registry.register(entry1_v1, entry1_v2)
    return registry


def test_iter(registry):
    """Validate iterating through an non-empty registry"""
    assert sorted(registry) == [(1, "1.0.0"), (1, "2.0.0")]


def test_register_invalid(registry):
    """Validate we cannot register an invalid value"""
    with pytest.raises(TypeError) as error:
        registry.register(2)
    assert str(error.value) == "Expected mapping, got int: 2"


def test_register_twice(registry, entry1_v1):
    """Validate an exception is raised if we try to register an entry twice."""
    with pytest.raises(AlreadyRegisteredError) as error:
        registry.register(entry1_v1)
    assert str(error.value) == "%s is already registered" % entry1_v1


def test_unregister(registry, entry1_v1):
    """Validate we can unregister an entry"""
    registry.unregister(entry1_v1)
    assert sorted(registry) == [(1, "2.0.0")]


def test_unregister_invalid(registry_empty, entry1_v1):
    """Validate an exception is raised when trying to unregister an invalid entry"""
    with pytest.raises(NotRegisteredError) as error:
        registry_empty.unregister(entry1_v1)
    assert str(error.value) == "%s is not registered" % entry1_v1


def test_get_versions(registry, entry1_v1):
    """Validate we can access a version stream from a uid"""
    assert isinstance(registry[entry1_v1.uid], VersionStream)


def test_get_version(registry, entry1_v1, entry1_v2):
    """Validate we can access a version stream from it's version"""
    assert registry[entry1_v1.uid][entry1_v2.version] is entry1_v2


def test_get_version_latest(registry, entry1_v1, entry1_v2):
    """Validate we can access the latest version of a stream."""
    assert registry[entry1_v1.uid].latest is entry1_v2


def test_find_by_uid(registry, entry1_v2):
    """Validate we can find an entry by it's uid."""
    assert registry.find(uid=1) is entry1_v2


def test_find_by_name(registry, entry1_v2):
    """Validate we can find an entry by it's name."""
    assert registry.find(name="testComponent") is entry1_v2


def test_find_by_name_and_version(registry, entry1_v1):
    """Validate we can find an entry by it's name and version."""
    assert registry.find(name="testComponent", version="1.0.0") == entry1_v1


def test_find_fail_no_match(registry):
    """Validate we raise if Registry.find find no match."""
    with pytest.raises(LookupError) as error:
        registry.find(name="an_unregistered_name")
    assert str(error.value) == "Found no compound matching requirements."


def test_find_fail_no_query(registry):
    """Validate we raise if Registry.find is called without any query."""
    with pytest.raises(ValueError) as error:
        registry.find(version=1)  # a version is not enough
    assert str(error.value) == "Should at least have one query."
