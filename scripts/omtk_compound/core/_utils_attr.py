"""
Majority of functions in theses libs could be refactored.
"""
import re
from contextlib import contextmanager

import pymel.core as pymel
from maya import OpenMaya, cmds, mel


def hold_connections(attrs, hold_inputs=True, hold_outputs=True):
    """
    Disconnect all inputs from the provided attributes but keep their in memory
    for ulterior re-connection.

    :param attrs: A list of pymel.Attribute instances.
    :type attrs: list of pymel.Attribute
    :param bool hold_inputs: Should we disconnect input connections?
    :param bool hold_outputs: Should we disconnect output connections?
    :return: The origin source and destination attribute for each entries.
    :rtype:list(tuple(src, str)
    """
    result = []
    for attr in attrs:
        if hold_inputs:
            attr_src = next(iter(attr.inputs(plugs=True)), None)
            if attr_src:
                pymel.disconnectAttr(attr_src, attr)
                result.append((attr_src, attr))
        if hold_outputs:
            for attr_dst in attr.outputs(plugs=True):
                pymel.disconnectAttr(attr, attr_dst)
                result.append((attr, attr_dst))

    return result


def fetch_connections(data):
    """
    Reconnect all attributes using returned data from the hold_connections function.
    :param data: A list of tuple of size-two containing pymel.Attribute instances.
    """
    for attr_src, attr_dst in data:
        pymel.connectAttr(attr_src, attr_dst)


@contextmanager
def context_disconnected_attrs(attrs, hold_inputs=True, hold_outputs=True):
    """
    A context (use with the 'with' statement) to apply instruction while ensuring
    the provided attributes are disconnected temporarily.

    :param attrs: Redirected to hold_connections.
    :type attrs: Sequence[pymel.Attribute]
    :param bool hold_inputs: Should we disconnect input connections?
    :param bool hold_outputs: Should we disconnect output connections?
    :return: A context that temporary disconnect attributes
    :rtype: Generator
    """
    data = hold_connections(attrs, hold_inputs=hold_inputs, hold_outputs=hold_outputs)
    yield
    fetch_connections(data)


def transfer_attribute(src_node, dst_node, src_name, dst_name=None):
    """
    Copy an existing attribute from a node to another.

    :param str src_node: The source node
    :param str dst_node: The destination node
    :param str src_name: The name of the attribute to transfer
    :param str dst_name: An optional name of the destination attribute
    :return: The dagpath of the newly created attribute
    """
    dst_name = dst_name or src_name
    src_path = "%s.%s" % (src_node, src_name)
    dst_path = "%s.%s" % (dst_node, dst_name)

    # Get MFnAttribute
    # TODO: Do it without pymel
    src_attr = pymel.Attribute(src_path)
    mfn_attr = src_attr.__apimattr__()

    # Compound attribute need to be handled differently
    if src_attr.isCompound():
        mfn_attr = OpenMaya.MFnCompoundAttribute(mfn_attr.object())
        mel_cmds = []
        mfn_attr.getAddAttrCmds(mel_cmds)
    else:
        mel_cmd = mfn_attr.getAddAttrCmd()
        # If we are transferring a child attribute we want to ignore any parent he might have.
        # Sadly modifying the mel script seem like the most simple way atm.
        if src_attr.isChild():
            mel_cmd = re.sub(r'-p "\w+"', "", mel_cmd)
        mel_cmds = [mel_cmd]

    # TODO: Rename attribute with regex?

    # Add the attribute on the input
    cmds.select(dst_node)
    for mel_cmd in mel_cmds:
        mel.eval(mel_cmd)

    return dst_path
