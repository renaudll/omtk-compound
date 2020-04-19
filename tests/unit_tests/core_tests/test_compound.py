"""
Tests for omtk_compound.core._compound
"""
# pylint: disable=redefined-outer-name
import os

import pytest
from maya import cmds as cmds_

from omtk_compound.core import Compound

_MAYA_DEFAULT_NODES = None


def _ls(**kwargs):  # todo: move to a pytest helper module, how does that work again?
    """
    Wrapper around cmds.ls that return a set of nodes without thoses
    that already  exist in an empty scene.
    """
    result = set(cmds_.ls(**kwargs))
    result -= _MAYA_DEFAULT_NODES
    return result


@pytest.fixture(scope="session")
def maya_standalone(maya_standalone):
    """
    After Maya initialization, store the defaults nodes so they can be
    excluded from `_ls` return.
    """
    global _MAYA_DEFAULT_NODES  # pylint: disable=global-statement
    _MAYA_DEFAULT_NODES = set(cmds_.ls())
    return maya_standalone


@pytest.fixture
def scene_empty_compound(cmds):
    """Fixture for a Maya scene with one empty compound."""
    cmds.namespace(addNamespace="test")
    cmds.createNode("network", name="test:inputs")
    cmds.createNode("network", name="test:outputs")


@pytest.fixture
def scene(cmds):
    """Fixture for a Maya scene with one compound containing one node."""
    cmds.namespace(addNamespace="test")
    cmds.createNode("network", name="test:inputs")
    cmds.createNode("network", name="test:outputs")
    cmds.createNode("transform", name="test:foobar")


@pytest.fixture
def scene_complex(cmds):
    """
    Fixture for a Maya scene with one compound and connections from inside and outside.
    """
    cmds.namespace(addNamespace="test")
    cmds.createNode("transform", name="inputs")
    cmds.createNode("network", name="test:inputs")
    cmds.createNode("transform", name="test:body")
    cmds.createNode("network", name="test:outputs")
    cmds.createNode("transform", name="outputs")

    cmds.addAttr("test:inputs", longName="testInput")
    cmds.addAttr("test:outputs", longName="testOutput")
    cmds.connectAttr("inputs.translateX", "test:inputs.testInput")
    cmds.connectAttr("test:inputs.testInput", "test:body.translateX")
    cmds.connectAttr("test:body.translateX", "test:outputs.testOutput")
    cmds.connectAttr("test:outputs.testOutput", "outputs.translateX")


@pytest.fixture
def compound(scene):  # pylint: disable=unused-argument
    """Fixture for a compound instance"""
    return Compound("test")


@pytest.fixture
def compound2(scene_complex):  # pylint: disable=unused-argument
    """Fixture for another compound instance"""
    # TODO: Merge with Component1?
    return Compound("test")


@pytest.mark.usefixtures("scene")
def test_init():
    """Validate we can create a compound object from an existing namespace."""
    assert Compound("test")


def test_str(compound):
    """Validate we can represent a compound as a string"""
    assert str(compound) == "<Compound 'test'>"


def test_input(compound):
    """Validate the `input` property"""
    assert compound.input == "test:inputs"


def test_output(compound):
    """Validate the `output` property"""
    assert compound.output == "test:outputs"


def test_inputs(compound):
    """Validate the `inputs` property"""
    assert compound.inputs == []


def test_outputs(compound):
    """Validate the `outputs` property"""
    assert compound.outputs == []


def test_nodes(compound):
    """Validate iterating through a compound will yield it's nodes."""
    assert set(compound) == {"test:inputs", "test:outputs", "test:foobar"}


def test_metadata(compound):
    """Validate we can get and set a compound metadata."""
    expected = {
        "int": 4,
        "float": 3.14159,
        "string": "Hello World",
        "bool": True,
        "NoneType": None,
        "list": ["some", "list", "elements"],
    }
    compound.set_metadata(expected)
    actual = compound.get_metadata()
    assert actual == expected


def test_iter(compound):  # TODO: not the same thing is above?
    """Validate if we iterate through a compound we yield it's node dagpaths."""
    assert tuple(iter(compound)) == tuple(compound)


def test_count(compound):
    """Validate the `count` method"""
    assert len(compound) == 3  # TODO: Do we want to count inn and out?


def test_explode(cmds, compound):
    """Validate we can explode a compound."""
    compound.explode()

    # Validate the compound bounds are removed
    assert not _ls(type="network")

    # Validate the compound internals still exist
    assert _ls(type="transform") == {"test:foobar"}

    # Validate the namespace still exist
    assert cmds.namespace(exists="test")


def test_explode_namespace(cmds, compound):
    """
    Validate exploding a compound with remove_namespace=True
    actually remove the namespace.
    """
    compound.explode(remove_namespace=True)

    # Validate the compound bounds are removed
    assert not cmds.ls(type="network")

    # Validate the compound internals still exist but with no namespace
    assert _ls(type="transform") == {"foobar"}

    # Validate the namespace still exist
    assert not cmds.namespace(exists="test")


@pytest.mark.usefixtures("cmds")
def test_explode_connections(compound2):
    """Validate exploding a compound preserve the connections."""
    compound2.explode()


@pytest.mark.usefixtures("cmds")
def test_export(compound, tmp_path):
    """Validate we can export a compound"""
    path = str(tmp_path / "compound.ma")
    compound.export(path)
    assert os.path.exists(path)


def test_delete(cmds, compound):
    """Validate we can delete a compound"""
    compound.delete()
    assert not cmds.namespace(exists=compound.namespace)
    assert not _ls(type="network")


def test_add_input_attr(cmds, compound):
    """Validate we can add attribute to the input node."""
    compound.add_input_attr("testInput")

    assert cmds.objExists("test:inputs.testInput")
    assert cmds.getAttr("test:inputs.testInput", type=True) == "double"


def test_add_output_attr(cmds, compound):
    """Validate we can add attribute to the output node."""
    compound.add_output_attr("testOutput")

    assert cmds.objExists("test:outputs.testOutput")
    assert cmds.getAttr("test:outputs.testOutput", type=True) == "double"


@pytest.mark.usefixtures("cmds")
def test_has_input_attr(compound):
    """Validate we can query if a compound have a certain input attribute."""
    assert not compound.has_input_attr("testInput")
    compound.add_input_attr("testInput")
    assert compound.has_input_attr("testInput")


@pytest.mark.usefixtures("cmds")
def test_has_output_attr(compound):
    """Validate we can query if a compound have a certain output attribute."""
    assert not compound.has_output_attr("testOutput")
    compound.add_output_attr("testOutput")
    assert compound.has_output_attr("testOutput")


@pytest.mark.usefixtures("cmds")
def test_get_connections(compound2):
    """Validate we can get a compound connections."""
    actual = compound2.get_connections()
    expected = (
        {u"test:inputs.testInput": [u"inputs.translateX"]},
        {u"test:outputs.testOutput": [u"outputs.translateX"]},
    )
    assert actual == expected


def test_hold_connections(cmds, compound2):
    """Validate we can hold a compound connections."""
    assert cmds.isConnected("inputs.translateX", "test:inputs.testInput")
    assert cmds.isConnected("test:outputs.testOutput", "outputs.translateX")
    compound2.hold_connections()
    assert not cmds.isConnected("inputs.translateX", "test:inputs.testInput")
    assert not cmds.isConnected("test:outputs.testOutput", "outputs.translateX")


def test_fetch_connections(cmds, compound2):
    """Validate we can fetch a compound connections."""
    # TODO: Better unit tests?
    assert cmds.isConnected("inputs.translateX", "test:inputs.testInput")
    assert cmds.isConnected("test:outputs.testOutput", "outputs.translateX")
    connections = compound2.hold_connections()
    compound2.fetch_connections(*connections)
    assert cmds.isConnected("inputs.translateX", "test:inputs.testInput")
    assert cmds.isConnected("test:outputs.testOutput", "outputs.translateX")


def test_optimize(compound):
    """Validate optimizing a compound raise a NotImplementedError"""
    # TODO: Write test
    with pytest.raises(NotImplementedError):
        compound.optimize()
