"""Tests for creation of compounds from various sources."""
# pylint: disable=redefined-outer-name
import pytest
from maya import cmds

from omtk_compound.core import (
    Compound,
    CompoundValidationError,
    create_empty,
    create_from_nodes,
    from_attributes,
    from_namespace,
)

_MAYA_DEFAULT_NODES = None


def _ls(**kwargs):
    """
    Wrapper around cmds.ls that return a set of nodes without thoses that
    already exist in an empty scene.
    """
    result = set(cmds.ls(**kwargs))
    result -= _MAYA_DEFAULT_NODES
    return result


@pytest.fixture(scope="session")
def maya_standalone(maya_standalone):
    """
    After Maya initialization, store the defaults nodes
    so they can be excluded from `_ls` return.
    """
    global _MAYA_DEFAULT_NODES  # pylint: disable=global-statement
    _MAYA_DEFAULT_NODES = set(cmds.ls())
    return maya_standalone


@pytest.fixture
def scene(maya_scene):  # pylint: disable=unused-argument
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


@pytest.mark.usefixtures("scene")
def test_create_from_nodes():
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


@pytest.mark.usefixtures("scene")
def test_create_from_nodes_namespaces():
    """Validate we can create a compound from a set of nodes and namespace them."""
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


@pytest.mark.usefixtures("scene")
def test_create_from_nodes_nested():
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


@pytest.mark.usefixtures("scene")
def test_create_from_nodes_nested_2():
    """
    Validate we can create a compound from a set of nodes containing another compound.
    """
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


def test_create_from_nodes_expose_reused_input_attributes(cmds):
    """ Ensure that we re-use an attribute if it is used twice as the network input.
    """
    cmds.createNode("transform", name="input1")
    cmds.createNode("transform", name="node1")
    cmds.createNode("transform", name="node2")

    cmds.connectAttr("input1.translateX", "node1.translateX")
    cmds.connectAttr("input1.translateX", "node2.translateX")

    create_from_nodes({"node1", "node2"}, namespace="test_namespace", expose=True)

    assert _ls() == {
        "input1",
        "test_namespace:inputs",
        "test_namespace:node1",
        "test_namespace:node2",
        "test_namespace:outputs",
    }
    assert cmds.listAttr("test_namespace:inputs", userDefined=True) == ["translateX"]
    assert not cmds.listAttr("test_namespace:outputs", userDefined=True)


def test_map_from_nodes_expose_simple(cmds):
    """ Ensure we can create a compound from existing nodes."""
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


@pytest.mark.usefixtures("scene")
def test_create_from_attributes():
    """
    Validate that we can create compounds form an attribute map that define
    it's inputs and outputs.
    """
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


@pytest.mark.usefixtures("scene")
def test_create_from_attributes_with_namespace():
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


@pytest.mark.usefixtures("scene")
def test_from_namespace_node_name():
    """
    Validate we raise an error if we try to create a compound from a namespace
    used by a node name.
    """
    with pytest.raises(ValueError) as error:
        from_namespace("a")

    assert str(error.value) == "A node is already named 'a'"


def test_from_namespace_non_existent_namespace():
    """
    Validate we raise an error if we try to create a compound from a namespace
    that does not exist.
    """
    with pytest.raises(ValueError) as error:
        from_namespace("a_namespace_that_do_not_exist")

    assert (
        str(error.value) == "Namespace 'a_namespace_that_do_not_exist' does not exist."
    )


def test_from_namespace_missing_input():
    """
    Validate we raise an error if try to crete a compound from a namespace
    without the input node.
    """
    cmds.namespace(addNamespace=":a")
    cmds.createNode("transform", name=":a:inputs")

    with pytest.raises(CompoundValidationError) as error:
        from_namespace("a")

    assert str(error.value) == "'a:outputs' don't exist."


def test_from_namespace_missing_output():
    """
    Validate we raise an error if try to crete a compound from a namespace
    without the output node.
    """
    cmds.namespace(addNamespace=":a")
    cmds.createNode("transform", name=":a:outputs")

    with pytest.raises(CompoundValidationError) as error:
        from_namespace("a")

    assert str(error.value) == "'a:inputs' don't exist."
