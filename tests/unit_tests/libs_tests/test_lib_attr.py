from maya import cmds

from omtk_compound.core._utils_attr import transfer_attribute


def test_transfer_attribute_single_scalar():
    """ Validate we can transfer a simple scalar attribute.
    """
    src = cmds.createNode("transform", name="src")
    dst = cmds.createNode("transform", name="dst")
    cmds.addAttr(src, longName="test")

    transfer_attribute(src, dst, "test")

    assert cmds.objExists("dst.test")
    # TODO: Validate more about the attribute?


def test_transform_attribute_child_scalar_to_single_scalar():
    """ Validate we can transfer an attribute child of another attribute to a single isolated attribute.
    """
    src = cmds.createNode("transform", name="src")
    dst = cmds.createNode("transform", name="dst")
    cmds.addAttr(src, longName="test", at="float2")
    cmds.addAttr(src, longName="testX", at="float", parent="test")
    cmds.addAttr(src, longName="testY", at="float", parent="test")

    transfer_attribute(src, dst, "testY")

    assert cmds.objExists("dst.testY")
