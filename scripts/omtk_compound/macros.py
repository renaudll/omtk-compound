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
_GUI_COMPOUND_PUBLISHER = None
_GUI_COMPOUND_MANAGER = None
_GUI_COMPOUND_EDITOR = None


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
    from omtk_compound.widgets.form_compound_publish import FormPublishCompound

    global _GUI_COMPOUND_PUBLISHER

    inst = _get_compound_from_selection()
    _GUI_COMPOUND_PUBLISHER = FormPublishCompound(inst)
    _GUI_COMPOUND_PUBLISHER.show()


def show_compound_manager():
    """Manage multiple compounds"""
    from omtk_compound.widgets.form_compound_manager import FormCompoundManager

    global _GUI_COMPOUND_MANAGER

    _GUI_COMPOUND_MANAGER = FormCompoundManager(manager)
    _GUI_COMPOUND_MANAGER.show()


def show_compound_editor():
    """Manage multiple compounds"""
    from omtk_compound.widgets.form_compound_editor import FormCompoundEditor

    global _GUI_COMPOUND_EDITOR

    inst = _get_compound_from_selection()
    _GUI_COMPOUND_EDITOR = FormCompoundEditor(inst)
    _GUI_COMPOUND_EDITOR.show()
