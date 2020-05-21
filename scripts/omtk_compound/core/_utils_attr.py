"""
Majority of functions in theses libs could be refactored.
"""
import logging
import re
from contextlib import contextmanager

import pymel.core as pymel
from maya import OpenMaya, cmds, mel

from . import _utils_namespace

_LOG = logging.getLogger(__name__)


def expose_attribute(
    src_node, dst_node, src_name, dst_name=None
):  # pylint: disable=too-many-locals
    """
    Copy an existing attribute from a node to another.

    :param str src_node: The source node
    :param str dst_node: The destination node
    :param str src_name: The name of the attribute to transfer
    :param str dst_name: An optional name of the destination attribute
    :return: The dagpath of the newly created attribute
    """
    # TODO: Simplify logic
    src_name = src_name.split("[", 1)[0]  # remove [0]  # HACK
    dst_name = dst_name or src_name
    dst_name = dst_name.split("[", 1)[0]  # remove [0]  # HACK
    src_path = "%s.%s" % (src_node, src_name)

    # Get MFnAttribute
    src_attr = pymel.Attribute(src_path)  # TODO: Remove pymel usage
    root_attr = src_attr.array() if src_attr.isElement() else src_attr
    attr_long_name = root_attr.longName()
    attr_short_name = root_attr.shortName()

    _LOG.debug("Exposed attribute is %r", root_attr)

    existing_long_names = cmds.listAttr(str(dst_node))
    existing_short_names = cmds.listAttr(str(dst_node), shortNames=True)

    _LOG.debug("Existing long names: %s", existing_long_names)
    _LOG.debug("Existing short names: %s", existing_short_names)

    unique_long_name = _utils_namespace.get_unique_namespace(
        attr_long_name, existing_long_names
    )
    unique_short_name = _utils_namespace.get_unique_namespace(
        attr_short_name, existing_short_names
    )

    dst_path_conformed = "%s.%s" % (dst_node, unique_long_name)
    _LOG.debug("Conformed %r to %r", dst_name, unique_short_name)

    # Generic attribute (Tdatacompound) cannot be constructed in MEL.
    # TODO: Use the OpenMaya method as the only transfer method?
    if src_attr.type() == "generic":
        _expose_generic_attribute(
            src_attr, dst_node, unique_long_name, unique_short_name
        )
    else:
        _expose_attribute_mel(
            src_attr,
            dst_node,
            attr_long_name,
            attr_short_name,
            unique_long_name,
            unique_short_name,
        )

    return dst_path_conformed


def _expose_generic_attribute(attr, dst_node, dst_name, attr_short_name):
    """
    Transfer a GENERIC attribute from a node to another.

    :param attr: The attribute to transfer
    :type attr: pymel.Attribute
    :param str dst_node: The node to create the new attribute on
    :param str dst_name: The new attribute long name
    :param attr_short_name: The new attribute short name
    """
    old_mfn = OpenMaya.MFnGenericAttribute(attr.__apimobject__())

    accepts = [
        idx
        for idx in range(OpenMaya.MFnData.kInvalid + 1, OpenMaya.MFnData.kLast)
        if old_mfn.accepts(idx)
    ]

    new_mfn = OpenMaya.MFnGenericAttribute()
    new_mobject = new_mfn.create(dst_name, attr_short_name)
    for accept in accepts:
        new_mfn.addDataAccept(accept)

    new_mfn.setWritable(old_mfn.isWritable())
    new_mfn.setReadable(old_mfn.isReadable())
    new_mfn.setCached(old_mfn.isCached())
    new_mfn.setStorable(old_mfn.isStorable())

    node_mfn = pymel.PyNode(dst_node).__apimfn__()
    node_mfn.addAttribute(new_mobject)


def _expose_attribute_mel(  # pylint: disable=too-many-arguments
    attr, dst_node, old_long_name, old_short_name, new_long_name, new_short_name
):
    """
    Transfer an attribute from a node to another.
    Note that it don't work with generic attributes.

    :param attr: The attribute to transfer
    :type attr: pymel.Attribute
    :param str dst_node: The node to transfer to attribute to.
    :param str old_long_name: The attribute old long name
    :param str old_short_name: The attribute old short name
    :param str new_long_name: The attribute new long name
    :param str new_short_name: The attribute new short name
    """
    mfn_attr = attr.__apimattr__()

    # Compound attribute need to be handled differently
    if attr.isCompound():
        mfn_attr = OpenMaya.MFnCompoundAttribute(mfn_attr.object())
        mel_cmds = []
        mfn_attr.getAddAttrCmds(mel_cmds)

        # Rename the children parent attributes
        mel_cmds = [
            mel_cmd.replace('-p "%s"' % old_long_name, '-p "%s"' % new_long_name)
            for mel_cmd in mel_cmds
        ]

    else:
        mel_cmd = mfn_attr.getAddAttrCmd()

        # If we are transferring a child attribute,
        # we want to ignore any parent he might have.
        # Sadly modifying the mel script seem like the most simple way atm.
        if attr.isChild():
            mel_cmd = re.sub(r'-p "\w+"', "", mel_cmd)

        mel_cmds = [mel_cmd]

    # If our compound is an element of a multi-attribute,
    # we'll want to make the new attribute non-multi.
    # Sadly modifying the mel script seem like the most simple way atm.
    mel_cmds[0] = mel_cmds[0].replace(" -m ", " ")  # -m is for --multi attribute

    _LOG.info("Replacing long name %r by %r", old_long_name, new_long_name)
    mel_cmds = [
        # Note: Last quote (") is missing by purpose
        mel_cmd.replace('-ln "%s' % old_long_name, '-ln "%s' % new_long_name)
        for mel_cmd in mel_cmds
    ]

    _LOG.info("Replacing short name %r by %r", old_short_name, new_short_name)
    mel_cmds = [
        # Note: Last quote (") is missing by by purpose
        mel_cmd.replace('-sn "%s' % old_short_name, '-sn "%s' % new_short_name)
        for mel_cmd in mel_cmds
    ]
    # Run MEL payload
    cmds.select(dst_node)
    for mel_cmd in mel_cmds:
        _LOG.debug(mel_cmd)
        mel.eval(mel_cmd)


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


def reorder_attributes(node, attributes):
    """
    :param str node: The node containing the attributes to re-order
    :param attributes: The attributes names, sorted in the desired order
    """
    cmds.undoInfo(openChunk=True)
    for attribute in reversed(attributes):
        attr_path = "%s.%s" % (node, attribute)
        cmds.deleteAttr(attr_path)
    cmds.undoInfo(closeChunk=True)
    cmds.undo()
