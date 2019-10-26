"""
Factory providing compound instances.
"""
import logging

import pymel.core as pymel
from maya import cmds

from omtk_compound.core._compound import Compound
from omtk_compound.core._constants import (
    INPUT_NODE_NAME,
    OUTPUT_NODE_NAME,
    COMPOUND_DEFAULT_NAMESPACE,
)
from omtk_compound.core._utils import get_unique_key, pairwise
from omtk_compound.core import _utils_namespace

_LOG = logging.getLogger(__name__)


def create_empty(namespace=COMPOUND_DEFAULT_NAMESPACE):
    """
    Create a compound from nothing.

    :param str namespace: The desired namespace for the new compound.
    :return: A ``Component`` instance.
    :rtype: Compound
    """
    namespace = _utils_namespace.get_unique_namespace(namespace)

    # Create namespace if necessary
    if not cmds.namespace(exists=namespace):
        cmds.namespace(add=namespace)

    # Create bounds if necessary
    bound_inn_dagpath = "%s:%s" % (namespace, INPUT_NODE_NAME)
    bound_out_dagpath = "%s:%s" % (namespace, OUTPUT_NODE_NAME)
    if not cmds.objExists(bound_inn_dagpath):
        cmds.createNode("network", name=bound_inn_dagpath)
    if not cmds.objExists(bound_out_dagpath):
        cmds.createNode("network", name=bound_out_dagpath)

    return Compound(namespace)


def create_from_nodes(objs, namespace=COMPOUND_DEFAULT_NAMESPACE, expose=False):
    """
    Create a compound from a set of nodes.
    This will move the nodes inside of a namespace.

    This will move these nodes into a unique namespace and return a Component instance.
    :param List[str] objs: A list of objects to include in the compound.
    :param str namespace: An optional namespace for the compound.
    :param bool expose: Should we expose attributes from connection outside the nodes boundaries?
    :return: A compound object
    :rtype: Compound
    """
    # Conform objs to pynodes
    objs = [pymel.PyNode(obj) for obj in objs]

    common_namespace = _utils_namespace.get_common_namespace(objs)
    if common_namespace:
        namespace = "{0}:{1}".format(common_namespace, namespace)

    namespace = _utils_namespace.get_unique_namespace(namespace)
    cmds.namespace(add=namespace)

    # TODO: Ensure namespaces are always absolute, we don't want the current namespace to play any role here.
    # TODO: Error out if we are breaking a compound by splitting it in two?
    for obj in objs:
        new_name = _utils_namespace.join_namespace(
            namespace, _utils_namespace.relative_namespace(str(obj), common_namespace)
        )

        node_namespace = _utils_namespace.get_namespace(new_name)
        if node_namespace and not cmds.namespace(exists=node_namespace):
            cmds.namespace(add=node_namespace)

        obj.rename(new_name)

    # We need an hub in and hub_out
    # However we don't known about which attributes to expose so we'll just create the objects.
    # todo: do we want to automatically populate the hubs?
    hub_inn_dagpath = "{0}:{1}".format(namespace, INPUT_NODE_NAME)
    hub_out_dagpath = "{0}:{1}".format(namespace, OUTPUT_NODE_NAME)
    if not cmds.objExists(hub_inn_dagpath):
        cmds.createNode("network", name=hub_inn_dagpath)
    if not cmds.objExists(hub_out_dagpath):
        cmds.createNode("network", name=hub_out_dagpath)

    inst = Compound(namespace)

    if expose:
        inputs, outputs = _get_attributes_map_from_nodes(objs)
        for input_ in inputs:
            data = _hold_input_attributes(input_)
            new_attr = inst.expose_input_attr(input_)
            _fetch_input_attributes(new_attr, data)
        for output in outputs:
            data = _hold_output_attributes(output)
            new_attr = inst.expose_output_attr(output)
            _fetch_output_attributes(new_attr, data)

    return inst


def from_namespace(namespace):
    """
    Create a compound instance from a namespace.

    :param namespace:
    :return:
    :raises ValueError: If the namespace does not contain a valid compound.
    """
    if cmds.objExists(namespace):
        raise ValueError("A node is already named %r" % namespace)

    if not cmds.namespace(exists=namespace):
        raise ValueError("Namespace %r does not exist." % namespace)

    inst = Compound(namespace)
    inst.validate()
    return inst


def from_attributes(attrs_inn, attrs_out, dagnodes=None, namespace=COMPOUND_DEFAULT_NAMESPACE):
    """
    Create a compound from a set of provided input and output attributes.
    The network node will be automatically determined.

    :param attrs_inn:
    :type attrs_inn: list(str)
    :param List[pymel.Attribute] attrs_out:
    :type attrs_out: list(str)
    :param List[pymel.PyNode] dagnodes:
    :param str namespace:
    :return: A Component
    :rtype: Compound
    """
    # TODO: Remove pymel usage
    dagnodes = [pymel.PyNode(dagnode) for dagnode in dagnodes] if dagnodes else None
    attrs_inn = [pymel.Attribute(attr) for attr in attrs_inn]
    attrs_out = [pymel.Attribute(attr) for attr in attrs_out]

    attrs_inn_map = {}
    attrs_out_map = {}

    for attr in attrs_inn:
        # if attr in attrs_inn_map:
        #     continue
        attr_name = get_unique_key(str(attr.longName()), attrs_inn_map)
        attrs_inn_map[attr_name] = attr

    for attr in attrs_out:
        # if attr in attrs_out_map:
        #     continue
        attr_name = get_unique_key(str(attr.longName()), attrs_out_map)
        attrs_out_map[attr_name] = attr

    inst = _from_attributes_map(
        attrs_inn_map, attrs_out_map, dagnodes=dagnodes, namespace=namespace
    )
    return inst


def from_file(path, namespace=COMPOUND_DEFAULT_NAMESPACE):
    """
    Create a Component in the scene from a CompoundDefinition.

    :param str path: Path to a maya ascii file (.ma) to load.
    :param str namespace: The namespace to use for the compound.
    :return: A Component instance.
    :rtype: omtk_compound.core.Compound
    """
    namespace = _utils_namespace.get_unique_namespace(namespace)
    _LOG.info("Creating compound with namespace: %s", namespace)
    cmds.file(path, i=True, namespace=namespace)
    return from_namespace(namespace)


def _get_nodes_from_attributes(attrs_inn, attrs_out):
    """
    Determine the common history between attributes that would be used to create a compound.
    """
    hist_inn = set()
    hist_out = set()
    for attr_inn in attrs_inn:
        hist_inn.update(attr_inn.listHistory(future=True))
    for attr_out in attrs_out:
        hist_out.update(attr_out.listHistory(future=False))
    return hist_inn & hist_out


def _get_attributes_map_from_nodes(nodes):
    """
    Determine the attribute to expose from a set of node.

    :param nodes:
    :return:
    """
    # For now we don't want to deal with name mismatch so we'll again use pymel.
    nodes_pm = {pymel.PyNode(node) for node in nodes}
    # TODO: Ignore attributes that point back to the network.

    # Create an attribute map of the attributes we need to expose.
    map_inputs = []
    map_outputs = []

    input_connections = (
        cmds.listConnections(
            nodes, source=True, destination=False, connections=True, plugs=True
        )
        or []
    )
    output_connections = (
        cmds.listConnections(
            nodes, source=False, destination=True, connections=True, plugs=True
        )
        or []
    )

    for dst, src in pairwise(input_connections):
        if pymel.Attribute(src).node() in nodes_pm:
            continue
        map_inputs.append(dst)

    for src, dst in pairwise(output_connections):
        if pymel.Attribute(dst).node() in nodes_pm:
            continue
        map_outputs.append(src)

    return map_inputs, map_outputs


def _from_attributes_map(
    attrs_inn, attrs_out, dagnodes=None, namespace=COMPOUND_DEFAULT_NAMESPACE
):
    """
    Create a Component from existing nodes.

    :param attrs_inn: A dict(k, v) of public input attributes where k is attr name and v is the reference attribute.
    :type attrs_inn: dict(str, pymel.Attribute)
    :param attrs_out: A dict(k, v) of publish output attributes where k is attr name v is the reference attribute.
    :type attrs_out: dict(str, pymel.Attribute)
    :param dagnodes: A list of nodes to include in the compound.
    :type dagnodes: List[pymel.PyNode]
    :param str namespace: A str for the created compound namespace.
    :return: Component instance.
    :rtype: Compound
    """
    assert dagnodes is None or None not in dagnodes

    # Conform dagnodes to set
    dagnodes = set(dagnodes) if dagnodes is not None else set()

    additional_dagnodes = _get_nodes_from_attributes(
        attrs_inn.values(), attrs_out.values()
    )
    dagnodes.update(additional_dagnodes)

    inst = create_from_nodes(dagnodes, namespace=namespace)

    # Create the hub_inn attribute.
    for attr in attrs_inn.values():
        # Hold connections
        # TODO: Should the expose redirect attribute by itself???
        inputs = _hold_input_attributes(str(attr))
        newattr = inst.expose_input_attr(str(attr))
        _fetch_input_attributes(newattr, inputs)

    for attr in attrs_out.values():
        # Hold connections
        # TODO: Should the expose redirect attribute by itself???
        outputs = _hold_output_attributes(str(attr))
        newattr = inst.expose_output_attr(str(attr))
        _fetch_output_attributes(newattr, outputs)

    return inst


def _hold_input_attributes(attr):
    inputs = cmds.listConnections(attr, destination=False, plugs=True) or []
    for input_ in inputs:
        cmds.disconnectAttr(input_, attr)
    return inputs


def _fetch_input_attributes(attr, inputs):
    for input_ in inputs:
        cmds.connectAttr(input_, attr)


def _hold_output_attributes(attr):
    outputs = cmds.listConnections(attr, source=False, plugs=True) or []
    for output in outputs:
        cmds.disconnectAttr(attr, output)
    return outputs


def _fetch_output_attributes(attr, outputs):
    for output in outputs:
        cmds.connectAttr(attr, output)
