"""
High levels commands made to be called from a menu, shelf, hotkey or runtime command.
"""
from maya import cmds

from omtk_compound.core import _utils_namespace
from omtk_compound.core._utils import preserve_selection
from omtk_compound.core._factory import from_namespace, create_from_nodes
from omtk_compound import manager

# Maya garbage collector hack
_GUI_ADD_ATTRIBUTE = None
_GUI_PUBLISH_COMPONENT = None


def _get_compound_from_selection():
    """ Helper method that retrieve the currently selected compound.

    :return: The currently selected compound
    :rtype: omtk_compound.Compound
    :raises ValueError: If no compound could be resolved.
    """
    sel = cmds.ls(selection=True)
    namespace = _utils_namespace.get_common_namespace(sel)

    if not namespace:
        raise ValueError("Found no common namespace")

    return from_namespace(namespace)


def create_compound():
    """ Create a compound from selected nodes. """
    sel = cmds.ls(selection=True, long=True)
    if not sel:
        cmds.warning("No nodes selected")
        return

    with preserve_selection():
        create_from_nodes(sel, expose=True)


def update_compound():
    """ Update a compound to it's latest version. """
    inst = _get_compound_from_selection()
    manager.update_compound(inst)


def explode_compound():
    """ Explode the selected compound. """
    inst = _get_compound_from_selection()
    inst.explode(remove_namespace=True)


def show_form_add_attribute():
    """ Show a UI that help with attribute creation. """
    from omtk_compound.widgets.form_add_attribute import FormCreateAttribute

    global _GUI_ADD_ATTRIBUTE

    _GUI_ADD_ATTRIBUTE = FormCreateAttribute()
    _GUI_ADD_ATTRIBUTE.show()


def show_form_publish_compound():
    """ Publish the selected compound. """
    from omtk_compound.widgets.form_publish_compound import FormPublishCompound

    global _GUI_PUBLISH_COMPONENT

    inst = _get_compound_from_selection()
    _GUI_PUBLISH_COMPONENT = FormPublishCompound(inst)
    _GUI_PUBLISH_COMPONENT.show()
