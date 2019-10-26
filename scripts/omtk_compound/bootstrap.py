"""
Entry point for initializing omtk_compound from the userSetup.
"""
import logging
from maya import cmds

_LOG = logging.getLogger(__name__)
_LOG.setLevel(logging.DEBUG)

_ENTRIES = (
    (
        "Create compound",
        "create",
        "omtk_compound_create",
        "from omtk_compound import macros; macros.create_compound()",
    ),
    (
        "Explode compound",
        "explode",
        "omtk_compound_explode",
        "from omtk_compound import macros; macros.explode_compound()",
    ),
    (
        "Publish compound",
        "publish",
        "omtk_compound_publish",
        "from omtk_compound import macros; macros.show_form_publish_compound()",
    ),
    (
        "Update compound",
        "update",
        "omtk_compound_update",
        "from omtk_compound import macros; macros.update_compound()",
    ),
    (
        "Add attribute",
        "addAttr",
        "omtk_compound_add_attribute",
        "from omtk_compound import macros; macros.show_form_add_attribute()",
    ),
)


def create_runtime_commands():
    """ Register macros so they can be bind to hotkeys.
    """
    for label, _, fn_name, command in _ENTRIES:
        # Remove old command if necessary
        if cmds.runTimeCommand(fn_name, exists=True):
            cmds.runTimeCommand(fn_name, edit=True, delete=True)

        cmds.runTimeCommand(
            fn_name, annotation=label, commandLanguage="python", command=command
        )
        # cmds.nameCommand(fn_name, annotation=label, sourceType="mel", command=command)


def _initialize_shelf(shelf):
    """ Create a shelf, deleting the previous one if needed.

    :param shelf: The name of the shelf
    """
    if cmds.shelfLayout(shelf, exists=1):
        if cmds.shelfLayout(shelf, query=1, childArray=1):
            for each in cmds.shelfLayout(shelf, query=1, childArray=1):
                cmds.deleteUI(each)
    else:
        cmds.shelfLayout(shelf, parent="ShelfLayout")


def build_shelf():
    """ Build the omtk_compound shelf
    """
    _LOG.debug("Creating shelf")

    shelf_name = "omtk_compound"
    _initialize_shelf(shelf_name)

    for label, label_short, fn_name, _ in _ENTRIES:
        cmds.setParent(shelf_name)
        cmds.shelfButton(
            image="commandButton.png",
            imageOverlayLabel=label_short,
            annotation=label,
            command=fn_name,
            sourceType="mel",
        )


def bootstrap():
    """ Main entry point for initialization. Called from userSetup.py.
    """
    create_runtime_commands()
    build_shelf()
