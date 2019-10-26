"""
High level integration tests
"""
import pymel.core as pymel
import pytest
from maya import cmds

from omtk_compound.core import (
    CompoundDefinition,
    Registry,
    create_from_nodes,
    Preferences,
    Manager,
)


@pytest.fixture
def registry():
    return Registry()


@pytest.fixture
def preferences(tmpdir):
    return Preferences(compound_location=str(tmpdir))


@pytest.fixture
def manager(registry, preferences):
    return Manager(registry=registry, preferences=preferences)


def test_integration_1(manager):
    """
    1) Create a compound
    2) Register the compound
    3) Modify the compound
    4) Register a new version of the compound
    5) Rollback to the previous version
    6) Update to latest
    """

    def _test_compound_v1():
        """
        Validate the namespace actually contain v1 of our test compound.

        :param str namespace: The compound namespace
        """
        # Validate internal connections
        for src, dst in (
            ("foo:inputs.input1X", "foo:multiplyDivide1"),
            ("foo:multiplyDivide1.outputX", "foo:outputs.outputX"),
        ):
            cmds.isConnected(src, dst)

        # Validate external connections
        for src, dst in (
            ("testInn.translateX", "foo:inputs.input1X"),
            ("foo:outputs.outputX", "testOut.translateX"),
        ):
            cmds.isConnected(src, dst)

        # Validate scene content
        for dagpath in (
            "foo:inputs",
            "foo:inputs.input1X",
            "foo:multiplyDivide1",
            "foo:outputs",
            "foo:outputs.outputX",
        ):
            assert cmds.objExists(dagpath)

        for dagpath in ("foo:outputs.outputY",):
            assert not cmds.objExists(dagpath)

    def _test_compound_v2():
        for dagpath in (
            "foo:inputs",
            "foo:inputs.input1X",
            "foo:multiplyDivide1",
            "foo:outputs",
            "foo:outputs.outputX",
            "foo:outputs.outputY",
        ):
            assert cmds.objExists(dagpath)

    # 1) Create a simple network
    mult1 = pymel.createNode("multiplyDivide")

    # Create a compound from the network
    compound = create_from_nodes([mult1], namespace="foo")
    a = mult1.input1X
    compound.expose_input_attr(a)
    compound.expose_output_attr(mult1.outputX)

    # Create connections from outside the compound
    cmds.createNode("transform", name="testInn")
    cmds.createNode("transform", name="testOut")
    cmds.connectAttr("testInn.translateX", "foo:inputs.input1X")
    cmds.connectAttr("foo:outputs.outputX", "testOut.translateX")

    _test_compound_v1()

    # Register the compound?
    compound_def_1 = CompoundDefinition(
        name="compound_name", version="1.0.0", uid="compound_uid"
    )
    compound.set_metadata(dict(compound_def_1))
    manager.publish_compound(compound)

    # Modify the scene content
    compound.expose_output_attr(mult1.outputY)

    _test_compound_v2()

    # TODO: Error if the file does not end with .ma?

    compound_def_2 = CompoundDefinition(
        name="compound_name", version="1.0.1", uid="compound_uid"
    )
    compound.set_metadata(dict(compound_def_2))
    manager.publish_compound(compound)

    cmds.connectAttr("foo:outputs.outputY", "testOut.translateY")

    # Downgrade our compound
    manager.update_compound(compound, "1.0.0")

    _test_compound_v1()

    # Upgrade our compound
    manager.update_compound(compound)
    _test_compound_v2()

    # Verify that we can restore our in-memory registry
    new_registry = Registry()
    new_registry.parse_directory(manager.preferences.compound_location)

    assert manager.registry == new_registry
