"""
Test cases for exposing an attribute.
"""
import pytest
from omtk_compound.core._utils_attr import expose_attribute
from omtk_compound import Compound


@pytest.fixture
def scene(cmds):
    """Fixture for a Maya scene with one compound containing one node."""
    cmds.namespace(addNamespace="test")
    cmds.createNode("network", name="test:inputs")
    cmds.createNode("network", name="test:outputs")
    cmds.createNode("transform", name="test:foobar")


@pytest.fixture
def compound(scene):
    return Compound("test")


def test_expose_element_attr(cmds):
    """Validate we can export an element attribute to a single attribute."""
    src = cmds.createNode("network", name="src")
    dst = cmds.createNode("network", name="dst")
    attr_name = "testMultiAttr"

    cmds.addAttr(src, longName=attr_name, multi=True)
    expose_attribute("%s.%s" % (src, attr_name), dst, attr_name)

    is_multi = cmds.attributeQuery(attr_name, node=dst, multi=True)
    assert not is_multi


def test_expose_input_attr(cmds, compound):
    """Validate we can expose an simple scalar compound attribute"""
    cmds.addAttr("test:foobar", longName="testAttr")
    compound.expose_input_attr("test:foobar.testAttr")
    assert cmds.objExists("test:inputs.testAttr")

    # Validate connection
    actual = cmds.connectionInfo("test:inputs.testAttr", destinationFromSource=True)[0]
    assert actual == "test:foobar.testAttr"


def test_expose_input_attr_non_readable(cmds, compound):
    """Validate that when we expose an unreadable input attribute it become readable."""
    cmds.addAttr("test:foobar", longName="testAttr", readable=False)
    compound.expose_input_attr("test:foobar.testAttr")

    assert cmds.attributeQuery("testAttr", node="test:inputs", readable=True)
    assert cmds.attributeQuery("testAttr", node="test:inputs", writable=True)


def test_expose_input_attr_non_writable(cmds, compound):
    """Validate that we cannot expose an un-writable attribute as an output"""
    cmds.addAttr("test:foobar", longName="testAttr", writable=False)
    with pytest.raises(ValueError) as error:
        compound.expose_input_attr("test:foobar.testAttr")

    assert (
        str(error.value)
        == "Cannot expose un-writable attribute 'test:foobar.testAttr' as an input."
    )


def test_expose_output_attr(cmds, compound):
    """Validate we can expose a simple scalar attribute as an output"""
    cmds.addAttr("test:foobar", longName="testAttr")
    compound.expose_output_attr("test:foobar.testAttr")
    assert cmds.objExists("test:outputs.testAttr")

    # Validate connection
    actual = cmds.connectionInfo("test:outputs.testAttr", sourceFromDestination=True)
    assert actual == "test:foobar.testAttr"


def test_expose_output_attr_non_readable(cmds, compound):
    """Validate that we cannot expose an un-readable attribute as an output"""
    cmds.addAttr("test:foobar", longName="testAttr", readable=False)
    with pytest.raises(ValueError) as error:
        compound.expose_output_attr("test:foobar.testAttr")

    assert (
        str(error.value)
        == "Cannot expose un-readable attribute 'test:foobar.testAttr' as an output."
    )


def test_expose_output_attr_non_writable(cmds, compound):
    """Validate that when we expose an un-writable output attribute it become writable."""
    cmds.addAttr("test:foobar", longName="testAttr", writable=False)
    compound.expose_output_attr("test:foobar.testAttr")

    assert cmds.attributeQuery("testAttr", node="test:outputs", readable=True)
    assert cmds.attributeQuery("testAttr", node="test:outputs", writable=True)
