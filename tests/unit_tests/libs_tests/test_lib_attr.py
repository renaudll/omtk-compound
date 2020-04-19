"""
Tests for omtk_compound.core._utils_attr
"""
from maya import cmds

from omtk_compound.core._utils_attr import expose_attribute, reorder_attributes


def test_transfer_attribute_single_scalar():
    """
    Validate we can transfer a simple scalar attribute.
    """
    src = cmds.createNode("transform", name="src")
    dst = cmds.createNode("transform", name="dst")
    cmds.addAttr(src, longName="test")

    expose_attribute(src, dst, "test")

    assert cmds.objExists("dst.test")
    # TODO: Validate more about the attribute?


def test_transform_attribute_child_scalar_to_single_scalar():
    """
    Validate we can transfer an attribute child of another attribute
    to a single isolated attribute.
    """
    src = cmds.createNode("transform", name="src")
    dst = cmds.createNode("transform", name="dst")
    cmds.addAttr(src, longName="test", at="float2")
    cmds.addAttr(src, longName="testX", at="float", parent="test")
    cmds.addAttr(src, longName="testY", at="float", parent="test")

    expose_attribute(src, dst, "testY")

    assert cmds.objExists("dst.testY")


def test_reorder_attributes():
    """
    Validate we can re-order attributes.
    """
    node = cmds.createNode("transform", name="testNode")
    cmds.addAttr(node, longName="testAttrA")
    cmds.addAttr(node, longName="testAttrB")

    assert cmds.listAttr(node, userDefined=True) == ["testAttrA", "testAttrB"]

    reorder_attributes(node, ["testAttrB", "testAttrA"])

    assert cmds.listAttr(node, userDefined=True) == ["testAttrB", "testAttrA"]
