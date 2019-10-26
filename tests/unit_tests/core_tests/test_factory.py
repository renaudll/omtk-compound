"""Tests for creation of compounds from various sources."""
import pytest
from maya import cmds

from omtk_compound.core import (
    Compound,
    ComponentValidationError,
    create_empty,
    create_from_nodes,
    from_attributes,
    from_namespace,
)

_MAYA_DEFAULT_NODES = None


def _ls(**kwargs):
    """Wrapper around cmds.ls that return a set of nodes without thoses that already exist in an empty scene."""
    result = set(cmds.ls(**kwargs))
    result -= _MAYA_DEFAULT_NODES
    return result


@pytest.fixture(scope="session")
def maya_standalone(maya_standalone):
    """After Maya initialization, store the defaults nodes so they can be excluded from `_ls` return."""
    global _MAYA_DEFAULT_NODES
    _MAYA_DEFAULT_NODES = set(cmds.ls())
    return maya_standalone


@pytest.fixture
def scene(maya_scene):
    """Simple scene with nodes connected in a "daisy chain"."""
    cmds.createNode("transform", name="a")
    cmds.createNode("transform", name="b")
    cmds.createNode("transform", name="c")
    cmds.createNode("transform", name="d")
    cmds.createNode("transform", name="e")

    cmds.connectAttr("a.translateX", "b.translateX")
    cmds.connectAttr("b.translateX", "c.translateX")
    cmds.connectAttr("c.translateX", "d.translateX")
    cmds.connectAttr("d.translateX", "e.translateX")


def test_create_empty():
    """Validate we can create a compound from nothing."""
    compound = create_empty()

    assert cmds.namespace(exists="compound1")
    assert isinstance(compound, Compound)
    assert _ls() == {"compound1:inputs", "compound1:outputs"}


def test_create_empty_multiple():
    """Validate behavior when creating multiple empty compounds."""
    create_empty()
    create_empty()
    create_empty()

    assert cmds.namespace(exists="compound1")
    assert cmds.namespace(exists="compound2")
    assert cmds.namespace(exists="compound3")
    assert _ls() == {
        "compound1:inputs",
        "compound1:outputs",
        "compound2:inputs",
        "compound2:outputs",
        "compound3:inputs",
        "compound3:outputs",
    }


def test_create_from_nodes(scene):
    """Validate we can create a compound from a set of nodes."""
    compound = create_from_nodes({"b", "c"})

    assert isinstance(compound, Compound)
    assert _ls() == {
        "a",
        "compound1:inputs",
        "compound1:outputs",
        "compound1:b",
        "compound1:c",
        "d",
        "e",
    }


def test_create_from_nodes_namespaces(scene):
    cmds.namespace(addNamespace="namespace")
    cmds.rename("a", "namespace:a")
    cmds.rename("b", "namespace:b")
    cmds.rename("c", "namespace:c")
    cmds.rename("d", "namespace:d")
    cmds.rename("e", "namespace:e")

    create_from_nodes({"namespace:c"}, namespace="new_namespace")

    assert _ls() == {
        "namespace:a",
        "namespace:b",
        "namespace:new_namespace:inputs",
        "namespace:new_namespace:c",
        "namespace:new_namespace:outputs",
        "namespace:d",
        "namespace:e",
    }


def test_create_from_nodes_nested(scene):
    """Validate we can create compound inside compound from a set of nodes."""
    create_from_nodes({"b", "c", "d"}, namespace="namespace_a")
    create_from_nodes({"namespace_a:c"}, namespace="namespace_b")

    assert _ls() == {
        "a",
        "namespace_a:inputs",
        "namespace_a:b",
        "namespace_a:namespace_b:inputs",
        "namespace_a:namespace_b:c",
        "namespace_a:namespace_b:outputs",
        "namespace_a:d",
        "namespace_a:outputs",
        "e",
    }


def test_create_from_nodes_nested_2(scene):
    create_from_nodes({"c"}, namespace="namespace_b")
    create_from_nodes(
        {"b", "namespace_b:c", "namespace_b:inputs", "namespace_b:outputs"},
        namespace="namespace_a",
    )

    assert _ls() == {
        "a",
        "namespace_a:inputs",
        "namespace_a:b",
        "namespace_a:namespace_b:inputs",
        "namespace_a:namespace_b:c",
        "namespace_a:namespace_b:outputs",
        "namespace_a:outputs",
        "d",
        "e",
    }


def test_map_from_nodes_expose_simple(cmds):
    cmds.createNode("transform", name="a")
    cmds.createNode("transform", name="b")
    cmds.createNode("transform", name="c")
    cmds.connectAttr("a.translateX", "b.translateX")
    cmds.connectAttr("b.translateY", "c.translateY")

    create_from_nodes(["b"], expose=True)

    assert _ls() == {"a", "compound1:inputs", "compound1:b", "compound1:outputs", "c"}

    for src, dst in (
        ("a.translateX", "compound1:inputs.translateX"),
        ("compound1:inputs.translateX", "compound1:b.translateX"),
        ("compound1:b.translateY", "compound1:outputs.translateY"),
        ("compound1:outputs.translateY", "c.translateY"),
    ):
        assert cmds.isConnected(src, dst)


def test_map_from_nodes_expose_cyclic(cmds):
    """ Validate we ignore connections pointing to nodes in the network."""
    cmds.createNode("transform", name="a")
    cmds.createNode("transform", name="b")
    cmds.createNode("transform", name="c")
    cmds.connectAttr("a.translateX", "b.translateX")
    cmds.connectAttr("b.translateY", "c.translateY")
    cmds.connectAttr("b.rotateX", "b.rotateY")

    create_from_nodes(["b"], expose=True)

    assert _ls() == {"a", "compound1:inputs", "compound1:b", "compound1:outputs", "c"}

    for src, dst in (
        ("a.translateX", "compound1:inputs.translateX"),
        ("compound1:inputs.translateX", "compound1:b.translateX"),
        ("compound1:b.translateY", "compound1:outputs.translateY"),
        ("compound1:outputs.translateY", "c.translateY"),
    ):
        assert cmds.isConnected(src, dst)


def test_create_from_attributes(scene):
    """Validate that we can create compounds form an attribute map that define it's inputs and outputs."""
    compound = from_attributes(["b.translateX"], ["d.translateX"])

    assert isinstance(compound, Compound)
    assert _ls() == {
        "a",
        "compound1:inputs",
        "compound1:b",
        "compound1:c",
        "compound1:d",
        "compound1:outputs",
        "e",
    }


def test_create_from_attributes_with_namespace(scene):
    """Validate we can create a compound from attributes in a namespace."""
    cmds.namespace(addNamespace=":namespace_a")
    cmds.rename("a", ":namespace_a:a")
    cmds.rename("b", ":namespace_a:b")
    cmds.rename("c", ":namespace_a:c")
    cmds.rename("d", ":namespace_a:d")
    cmds.rename("e", ":namespace_a:e")

    compound = from_attributes(
        [":namespace_a:b.translateX"], [":namespace_a:d.translateX"]
    )

    assert isinstance(compound, Compound)
    assert _ls() == {
        "namespace_a:a",
        "namespace_a:compound1:inputs",
        "namespace_a:compound1:b",
        "namespace_a:compound1:c",
        "namespace_a:compound1:d",
        "namespace_a:compound1:outputs",
        "namespace_a:e",
    }


def test_from_namespace_node_name(scene):
    """Validate we raise an error if we try to create a compound from a namespace used by a node name."""
    with pytest.raises(ValueError) as error:
        from_namespace("a")

    assert str(error.value) == "A node is already named 'a'"


def test_from_namespace_non_existent_namespace():
    """Validate we raise an error if we try to create a compound from a namespace that does not exist."""
    with pytest.raises(ValueError) as error:
        from_namespace("a_namespace_that_do_not_exist")

    assert (
        str(error.value) == "Namespace 'a_namespace_that_do_not_exist' does not exist."
    )


def test_from_namespace_missing_input():
    """Validate we raise an error if try to crete a compound from a namespace without the input node."""
    cmds.namespace(addNamespace=":a")
    cmds.createNode("transform", name=":a:inputs")

    with pytest.raises(ComponentValidationError) as error:
        from_namespace("a")

    assert str(error.value) == "'a:outputs' don't exist."


def test_from_namespace_missing_output():
    """Validate we raise an error if try to crete a compound from a namespace without the output node."""
    cmds.namespace(addNamespace=":a")
    cmds.createNode("transform", name=":a:outputs")

    with pytest.raises(ComponentValidationError) as error:
        from_namespace("a")

    assert str(error.value) == "'a:inputs' don't exist."
