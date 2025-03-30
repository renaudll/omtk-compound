import logging
import re
from contextlib import contextmanager
from typing import Generator

import pymel.core as pymel
from maya import OpenMaya, cmds, mel

from . import _utils_namespace

_LOG = logging.getLogger(__name__)


def expose_attribute(
    src_node: str, dst_node: str, src_name: str, dst_name: str = None
) -> str:
    src_name = src_name.split("[", 1)[0]
    dst_name = dst_name or src_name
    dst_name = dst_name.split("[", 1)[0]
    src_path = f"{src_node}.{src_name}"

    src_attr = pymel.Attribute(src_path)
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

    dst_path_conformed = f"{dst_node}.{unique_long_name}"
    _LOG.debug("Conformed %r to %r", dst_name, unique_short_name)

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


def _expose_generic_attribute(
    attr: pymel.Attribute, dst_node: str, dst_name: str, attr_short_name: str
) -> None:
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


def _expose_attribute_mel(
    attr: pymel.Attribute,
    dst_node: str,
    old_long_name: str,
    old_short_name: str,
    new_long_name: str,
    new_short_name: str,
) -> None:
    mfn_attr = attr.__apimattr__()

    if attr.isCompound():
        mfn_attr = OpenMaya.MFnCompoundAttribute(mfn_attr.object())
        mel_cmds = []
        mfn_attr.getAddAttrCmds(mel_cmds)

        mel_cmds = [
            mel_cmd.replace(f'-p "{old_long_name}"', f'-p "{new_long_name}"')
            for mel_cmd in mel_cmds
        ]

    else:
        mel_cmd = mfn_attr.getAddAttrCmd()

        if attr.isChild():
            mel_cmd = re.sub(r'-p "\w+"', "", mel_cmd)

        mel_cmds = [mel_cmd]

    mel_cmds[0] = mel_cmds[0].replace(" -m ", " ")
    _LOG.info("Replacing long name %r by %r", old_long_name, new_long_name)
    mel_cmds = [
        mel_cmd.replace(f'-ln "{old_long_name}', f'-ln "{new_long_name}')
        for mel_cmd in mel_cmds
    ]

    _LOG.info("Replacing short name %r by %r", old_short_name, new_short_name)
    mel_cmds = [
        mel_cmd.replace(f'-sn "{old_short_name}', f'-sn "{new_short_name}')
        for mel_cmd in mel_cmds
    ]
    cmds.select(dst_node)
    for mel_cmd in mel_cmds:
        _LOG.debug(mel_cmd)
        mel.eval(mel_cmd)


def hold_connections(
    attrs: list[pymel.Attribute], hold_inputs: bool = True, hold_outputs: bool = True
) -> list[tuple[pymel.Attribute, str]]:
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


def fetch_connections(data: list[tuple[pymel.Attribute, str]]) -> None:
    for attr_src, attr_dst in data:
        pymel.connectAttr(attr_src, attr_dst)


@contextmanager
def context_disconnected_attrs(
    attrs: list[pymel.Attribute], hold_inputs: bool = True, hold_outputs: bool = True
) -> Generator:
    data = hold_connections(attrs, hold_inputs=hold_inputs, hold_outputs=hold_outputs)
    yield
    fetch_connections(data)


def reorder_attributes(node: str, attributes: list[str]) -> None:
    cmds.undoInfo(openChunk=True)
    for attribute in reversed(attributes):
        attr_path = f"{node}.{attribute}"
        cmds.deleteAttr(attr_path)
    cmds.undoInfo(closeChunk=True)
    cmds.undo()
