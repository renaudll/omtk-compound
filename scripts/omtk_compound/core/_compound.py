"""
A Compound represents encapsulation in Maya
via a namespace and an input and output attribute holder networks.
"""

import ast
import logging
from typing import Generator
from maya import cmds
import pymel.core as pymel

from ._constants import INPUT_NODE_NAME, OUTPUT_NODE_NAME
from ._parser import remove_root_namespace, write_metadata_to_ma_file
from . import _utils_attr, _utils_namespace

_LOG = logging.getLogger(__name__)


class CompoundError(Exception):
    """Base class for a compound related error"""


class CompoundValidationError(CompoundError):
    """Exception raised when a compound object is invalid"""


class Compound:
    """An instance of a network of Maya nodes that represent encapsulation.
    It shares a common namespace and has input and output networks.
    """

    def __init__(self, namespace: str):
        """
        :param namespace: A namespace
        :raises CompoundValidationError: If the namespace doesn't contain a valid compound
        """
        self._inputs = {}
        self._outputs = {}
        self._nodes = set()
        self.dagpath = namespace
        self.namespace = namespace  # alias

        self.validate()

    def __str__(self) -> str:
        return "<Compound %r>" % self.dagpath

    def __len__(self) -> int:
        """The number of nodes inside the compound."""
        return len(self.nodes)

    def __iter__(self) -> Generator[str, None, None]:
        """
        :return: An iterator that yield the compound nodes dagpaths
        """
        return self.iter()

    def __melobject__(self) -> str:
        """The dagpath of a compound is its namespace.

        :return: The compound namespace, ex: 'namespace'
        """
        return self.dagpath

    @property
    def nodes(self) -> list[str]:
        """
        :return: The dagpath of all the nodes under the compound.
        """
        return cmds.ls("%s:*" % self.namespace)

    @property
    def input(self) -> str:
        """
        :return: The dagpath of the node containing the input attributes.
        """
        return ":".join((self.namespace, INPUT_NODE_NAME))

    @property
    def output(self) -> str:
        """
        :return: The dagpath of the node containing the output attributes.
        """
        return ":".join((self.namespace, OUTPUT_NODE_NAME))

    @property
    def inputs(self) -> list[str]:
        """
        :return: A list of the compound inputs attributes as dagpath
        """
        attr_names = cmds.listAttr(self.input, userDefined=True) or []
        prefix = self.input + "."
        return [prefix + attr_name for attr_name in attr_names]

    @property
    def outputs(self) -> list[str]:
        """
        :return: A list of the compound input attributes as dagpath
        """
        attr_names = cmds.listAttr(self.output, userDefined=True) or []
        prefix = self.output + "."
        return [prefix + attr_name for attr_name in attr_names]

    def validate(self) -> None:
        """Validate the compound. Raise an exception in case of failure.

        :raises CompoundValidationError: If the compound doesn't validate.
        """
        if self.namespace in ("UI",):
            raise CompoundValidationError(
                "Namespace %s is blacklisted." % (self.namespace)
            )
        if not cmds.objExists(self.input):
            raise CompoundValidationError("%r doesn't exist." % self.input)
        if not cmds.objExists(self.output):
            raise CompoundValidationError("%r doesn't exist." % self.output)

    def get_metadata(self) -> dict:
        """A compound can have associated metadata.
        This generally means an ID, a name, and a version, but it's all arbitrary.
        The metadata is stored in the input node.

        :return: A metadata dict
        """
        attr = "%s.notes" % self.input
        if not cmds.objExists(attr):
            return {}

        # TODO: Handle parsing failure
        # TODO: Handle spaces better
        metadata_str = cmds.getAttr(attr)
        lines = metadata_str.split("\n")
        metadata = {}
        for line in lines:
            key, val = line.split(":", 1)
            metadata[key] = ast.literal_eval(val)
        return metadata

    def set_metadata(self, metadata: dict):
        """Set the metadata stored in the compound as an attribute.

        :param metadata: The new metadata to set
        """
        attr = "%s.notes" % self.input

        # The notes attribute is created automatically by maya on first edition.
        # If it does exist, re-create it the same way.
        if not cmds.objExists(attr):
            cmds.addAttr(
                self.input,
                cachedInternally=True,
                shortName="nts",
                longName="notes",
                dataType="string",
            )

        lines = []
        for key, val in metadata.items():
            val = str(val) if isinstance(val, str) else val
            lines.append("%s:%r" % (key, val))
        metadata_str = "\n".join(lines)

        cmds.setAttr(attr, metadata_str, type="string")

    def iter(self) -> Generator[str, None, None]:
        """Iterate through nodes in the graph."""
        return iter(self.nodes)

    def export(self, path: str):
        """Export the compound to a file."""

        objs = tuple(self)
        # Hold current file
        current_path = cmds.file(q=True, sn=True)

        # Use maya.cmds instead of pymel
        input_ = self.input
        output = self.output

        # Collect input attributes, excluding 'message'
        grp_inn_attrs = {f"{input_}.{attr_name}" for attr_name in cmds.listAttr(input_, settable=True) or ()}
        grp_inn_attrs.discard('message')

        # Collect output attributes, excluding 'message'
        grp_out_attrs = {f"{output}.{attr_name}" for attr_name in cmds.listAttr(output, settable=True) or ()}
        grp_out_attrs.discard('message')

        with _utils_attr.context_disconnected_attrs(
            grp_inn_attrs, hold_inputs=True, hold_outputs=False
        ):
            with _utils_attr.context_disconnected_attrs(
                grp_out_attrs, hold_inputs=False, hold_outputs=True
            ):
                cmds.select(objs)
                cmds.file(rename=path)
                cmds.file(force=True, exportSelected=True, type="mayaAscii")

                # Hack: Rename current namespace from the file
                # TODO: Investigate any maya built-in option for that
                remove_root_namespace(self.namespace, path)

                write_metadata_to_ma_file(path, self.get_metadata())

                # Fetch current file
                cmds.file(rename=current_path)

    def delete(self):
        """Delete the content of a compound and its associated namespace(s)."""
        cmds.namespace(removeNamespace=self.namespace, deleteNamespaceContent=True)

    def optimize(self):
        """
        Implement optimization routines. Call before publishing rig to animation.

        There's multiple things that can be done here
        - Remove the inn and out hub.
        - Remove decomposeMatrix connected to composeMatrix
        - Remove composeMatrix connected to decomposeMatrix

        :raises NotImplementedError: Always
        """
        self.explode()

        raise NotImplementedError

    # --- Interface management ---

    def add_input_attr(self, long_name: str, **kwargs):
        """Wrapper around `cmds.addAttr` that creates an input attribute.

        :param long_name: Name of the attribute to create.
        :param kwargs: Keyword arguments are forwarded to `cmds.addAttr`
        """
        cmds.addAttr(self.input, longName=long_name, **kwargs)

    def add_output_attr(self, long_name: str, **kwargs):
        """Wrapper around `cmds.addAttr` that creates an output attribute.

        :param long_name: Name of the attribute to create.
        :param kwargs: Keyword arguments are forwarded to `cmds.addAttr`
        """
        cmds.addAttr(self.output, longName=long_name, **kwargs)

    def has_input_attr(self, attr_name: str) -> bool:
        """Check if a provided input attribute exists.

        :param attr_name: An attribute name
        :return: Does the attribute exist?
        """
        return cmds.objExists("%s.%s" % (self.input, attr_name))

    def has_output_attr(self, attr_name: str) -> bool:
        """Check if a provided output attribute exists.

        :param attr_name: An attribute name
        :return: Does the attribute exist?
        """
        return cmds.objExists("%s.%s" % (self.output, attr_name))

    def expose_input_attr(self, dagpath: str) -> str:
        """Expose an attribute as an input attribute of the compound.

        :param dagpath: The attribute to expose
        :return: The dagpath of the exposed attribute
        :raises: ValueError: If the attribute is already a connection destination
        """
        attr = pymel.Attribute(dagpath)
        dagpath = str(attr)

        attr = attr.array() if attr.isElement() else attr
        if not cmds.attributeQuery(
            attr.longName(), node=str(attr.node()), writable=True
        ):
            raise ValueError(
                "Cannot expose un-writable attribute %r as an input." % dagpath
            )

        if cmds.connectionInfo(dagpath, isDestination=True):
            raise ValueError("Cannot expose a destination attribute: %r" % dagpath)

        src_node = str(attr.node())
        src_dagpath = _utils_attr.expose_attribute(
            src_node, self.input, attr.longName()
        )

        mattr = pymel.Attribute(src_dagpath).__apimattr__()
        mattr.setReadable(True)

        cmds.connectAttr(src_dagpath, dagpath)

        return src_dagpath

    def expose_output_attr(self, dagpath: str) -> str:
        """
        Expose an attribute as an output attribute of the compound.

        :param dagpath: The attribute to expose
        :return: The dagpath of the exposed attribute
        :raises: ValueError: If the attribute is the source of an existing connection.
        """
        attr = pymel.Attribute(dagpath)
        dagpath = str(attr)

        attr_to_check = attr.array() if attr.isElement() else attr
        if not cmds.attributeQuery(
            attr_to_check.longName(), node=str(attr.node()), readable=True
        ):
            raise ValueError(
                "Cannot expose un-readable attribute %r as an output." % dagpath
            )

        if cmds.connectionInfo(dagpath, isSource=True):
            raise ValueError("Cannot expose a source attribute: %r" % dagpath)

        src_node = str(attr.node())
        attr_name = str(attr.longName())
        dst_dagpath = _utils_attr.expose_attribute(src_node, self.output, attr_name)

        mattr = pymel.Attribute(dst_dagpath).__apimattr__()
        mattr.setWritable(True)

        cmds.connectAttr(dagpath, dst_dagpath)

        return dst_dagpath

    def explode(self, remove_namespace: bool = False):
        """
        Delete the compound and its hub,
        remapping the attribute to their original location.

        :param remove_namespace: Should we remove the compound namespace?
        """

        def _remap_attr(attr_):
            attr_ = pymel.Attribute(attr_) if isinstance(attr_, str) else None
            attr_src = next(iter(attr_.inputs(plugs=True)), None)
            if attr_src:
                pymel.disconnectAttr(attr_src, attr_)
            for attr_dst in attr_.outputs(plugs=True):
                pymel.disconnectAttr(attr_, attr_dst)
                if attr_src:
                    pymel.connectAttr(attr_src, attr_dst, force=True)

        for attr in self.inputs:
            _remap_attr(attr)
        for attr in self.outputs:
            _remap_attr(attr)

        cmds.delete(self.input)
        cmds.delete(self.output)

        if remove_namespace:
            cmds.namespace(
                mergeNamespaceWithParent=True, removeNamespace=self.namespace
            )

    def get_connections(self) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
        """
        Return two dict(k,v) describing what is connected to the compound.
        This helps with updating/promoting compound.
        """

        def _conform(attr_):
            return str(attr_)

        map_inn = {}
        map_out = {}
        for attr in pymel.PyNode(self.input).listAttr(userDefined=True):
            if attr.isDestination():
                map_inn[_conform(attr)] = list(map(_conform, attr.inputs(plugs=True)))
        for attr in pymel.PyNode(self.output).listAttr(userDefined=True):
            if attr.isSource():
                map_out[_conform(attr)] = list(map(_conform, attr.outputs(plugs=True)))
        return map_inn, map_out

    def hold_connections(self) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
        """
        Disconnect the compound input and output connections.

        :return: The disconnected inputs and outputs connections.
        """
        map_inn, map_out = self.get_connections()

        for attr_dst, attr_srcs in map_inn.items():
            for attr_src in attr_srcs:
                cmds.disconnectAttr(attr_src, attr_dst)

        for attr_src, attr_dsts in map_out.items():
            for attr_dst in attr_dsts:
                cmds.disconnectAttr(attr_src, attr_dst)

        return map_inn, map_out

    @staticmethod
    def fetch_connections(map_inn: dict[str, list[str]], map_out: dict[str, list[str]]):
        """
        Reconnect the compound input and output connections.

        :param map_inn: Input connection to create
        :param map_out: Output connections to create
        """
        for attr_dst, attr_srcs in map_inn.items():
            for attr_src in attr_srcs:
                cmds.connectAttr(attr_src, attr_dst)

        for attr_src, attr_dsts in map_out.items():
            for attr_dst in attr_dsts:
                cmds.connectAttr(attr_src, attr_dst)

    def rename(self, namespace: str):
        """
        Change the compound namespace.

        :param namespace: The new namespace to use
        """
        old_namespace = self.namespace
        new_namespace = _utils_namespace.get_unique_namespace(namespace)
        cmds.namespace(addNamespace=new_namespace)
        cmds.namespace(moveNamespace=(self.namespace, new_namespace))
        cmds.namespace(removeNamespace=old_namespace)
        self.namespace = new_namespace

    def generate_docstring(self) -> str:
        """
        Generate a description from the compound interface.

        :return: A description
        """
        result = ""
        result += "Inputs:\n"
        for input_ in self.inputs:
            result += " -%s\n" % input_.split(".")[-1]
        result += "Outputs:\n"
        for output in self.outputs:
            result += " -%s\n" % output.split(".")[-1]
        return result
