"""
Tests for omtk_compound.core._utils_namespace
"""
import pytest

from omtk_compound.core._utils_namespace import (
    get_unique_namespace,
    get_common_namespace,
    relative_namespace,
    join_namespace,
)


def test_get_unique_namespace_no_suffix():
    """Assert case for a search without a numbered suffix."""
    actual = get_unique_namespace("test")
    assert actual == "test"


def test_get_unique_namespace_suffix():
    """Assert case for a search with a numbered suffix."""
    actual = get_unique_namespace("test1")
    assert actual == "test1"


def test_get_unique_namespace_nested():
    """Assert case for a search with nested compounds."""
    actual = get_unique_namespace("test:test1")
    assert actual == "test:test1"


def test_get_unique_namespace_clash_no_suffix(cmds):
    """Assert case for a search namespace without a numbered suffix."""
    cmds.namespace(addNamespace="test")
    actual = get_unique_namespace("test")
    assert actual == "test1"


def test_get_unique_namespace_clash_with_suffix(cmds):
    """Assert case for a search with a numbered suffix."""
    cmds.namespace(addNamespace="test1")
    actual = get_unique_namespace("test1")
    assert actual == "test2"


@pytest.mark.parametrize(
    "namespaces,expected",
    (
        (["a", "b"], "a:b"),
        ([":a", "b"], ":a:b"),
        ([":", "a"], ":a"),
        (["a", "b", "c"], "a:b:c"),
    ),
)
def test_join_namespace(namespaces, expected):
    """Ensure we can join two namespaces."""
    assert join_namespace(*namespaces) == expected


@pytest.mark.parametrize(
    "nodes,expected",
    (
        # no namespace
        (["a", "b", "c"], None),
        # namespace + no namespace
        (["namespace_1:a", "a"], None),
        # same namespaces
        (["namespace_1:a", "namespace_1:a"], "namespace_1"),
        # no common namespace
        (["namespace_1:a", "namespace_2:a"], None),
        # common parent namespace
        (["namespace_1:namespace_2:a", "namespace_1:b"], "namespace_1"),
    ),
)
def test_get_common_namespace_no_namespaces(nodes, expected):
    """Ensure we can get the common namespace between two namespaces."""
    assert get_common_namespace(nodes) == expected


@pytest.mark.parametrize(
    "namespace,parent_namespace, expected",
    (
        ("namespace_1:a", "namespace_1", "a"),
        ("namespace_1:namespace_2:a", "namespace_1:namespace_2", "a"),
        ("a", "namespace_1", "a"),
        ("namespace_1:a", "namespace_2", "namespace_1:a"),
    ),
)
def test_get_relative_namespace(namespace, parent_namespace, expected):
    """Ensure we can extract a relative namespace."""
    assert relative_namespace(namespace, parent_namespace) == expected
