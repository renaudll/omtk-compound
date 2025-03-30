"""
QWidget that lists compound instances in the scene.
"""

import logging
from maya import cmds
from omtk_compound import manager
from omtk_compound.core._factory import from_scene, from_file
from omtk_compound.vendor.Qt import QtCore, QtWidgets
from omtk_compound.widgets.ui import widget_compound_outliner as ui_def
from omtk_compound.models import CompoundManagerModel, DataRole
from omtk_compound.widgets.form_compound_picker import FormCompoundPicker

_LOG = logging.getLogger(__name__)


class CompoundOutlinerWidget(QtWidgets.QWidget):
    """
    QWidget that lists compound instances in the scene.
    """

    selectionChanged = QtCore.Signal(list)

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        # TODO: See if we can remove picker member
        self.picker: FormCompoundPicker | None = None
        self.ui = ui_def.Ui_Form()
        self.ui.setupUi(self)

        self.manager = manager
        compounds = tuple(from_scene())
        self.model = CompoundManagerModel(self.manager, entries=compounds)
        self.ui.treeView.setModel(self.model)
        self.selection_model = self.ui.treeView.selectionModel()
        self.selection_model.selectionChanged.connect(self.on_selection_changed)
        self.ui.treeView.customContextMenuRequested.connect(
            self.on_custom_context_menu_requested
        )

    def _get_selected_compounds(self) -> list:
        """
        :return: A list of selected compounds
        """
        indexes = self.selection_model.selectedRows()
        return [self.model.data(index, DataRole) for index in indexes]

    def on_selection_changed(self, *_) -> None:
        """
        Called when the compound selection changes.
        """
        objs = set()
        compounds = self._get_selected_compounds()
        for compound in compounds:
            objs.update(compound.nodes)
        cmds.select(list(objs))
        self.selectionChanged.emit(compounds)

    def on_custom_context_menu_requested(self, pos: QtCore.QPoint) -> None:
        """
        Called when the custom context menu is requested (on right click generally).

        :param pos: The position for the menu
        """
        menu = QtWidgets.QMenu(self)
        action_promote = QtWidgets.QAction("Promote To...", self)
        action_promote.triggered.connect(self.on_action_promote_selected)
        menu.addAction(action_promote)
        menu.exec_(self.ui.treeView.mapToGlobal(pos))

    def on_action_promote_selected(self) -> None:
        """
        Called when the user wants to promote a compound.
        """
        self.picker = FormCompoundPicker(self.manager.registry)
        self.picker.onPicked.connect(self._promote_selected)
        self.picker.exec_()

    def _promote_selected(self, compound_definition: dict) -> None:
        """
        Called when the user submits a compound to be promoted.
        :param compound_definition: The compound definition to promote to
        """
        compounds = self._get_selected_compounds()
        path = compound_definition["path"]

        for compound in compounds:
            # TODO: Move to shared function
            _LOG.info(f"Promoting {compound} to {compound_definition}")
            namespace = compound.namespace
            connections = compound.hold_connections()
            compound.delete()
            new_compound = from_file(path, namespace=namespace)
            new_compound.fetch_connections(*connections)
