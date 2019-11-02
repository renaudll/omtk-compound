from omtk_compound.core import create_from_nodes


def test_integration(cmds):
    """
    Test a complex case where:
    - We expose two element attributes from the same array
    """
    cmds.createNode("transform", name="inputs1")
    cmds.createNode("transform", name="inputs2")
    cmds.createNode("plusMinusAverage", name="util")
    cmds.createNode("transform", name="outputs")

    cmds.connectAttr("inputs1.translate", "util.input3D[0]")
    cmds.connectAttr("inputs2.translate", "util.input3D[1]")
    cmds.connectAttr("util.output3D", "outputs.translate")

    create_from_nodes(["util"], expose=True)
