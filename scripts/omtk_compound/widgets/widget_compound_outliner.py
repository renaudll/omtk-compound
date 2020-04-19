"""
QWidget that list compound instances in the scene.
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
    QWidget that list compound instances in the scene.
    """

    selectionChanged = QtCore.Signal(list)

    def __init__(self, parent=None):
        """
        :param omtk_compound.Manager manager: A manager instance
        """
        super(CompoundOutlinerWidget, self).__init__(parent)

        # TODO: See if we can remove picker member
        self.picker = None

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

    def _get_selected_compounds(self):
        """
        :return: A list of selected compounds
        :rtype: List[omtk_compound.Compounds]
        """
        indexes = self.selection_model.selectedRows()
        return [self.model.data(index, DataRole) for index in indexes]

    def on_selection_changed(self, *_):
        """
        Called when the compound selection changed.
        """
        objs = set()
        compounds = self._get_selected_compounds()
        for compound in compounds:
            objs.update(compound.nodes)
        cmds.select(list(objs))
        self.selectionChanged.emit(compounds)

    def on_custom_context_menu_requested(self, pos):
        """
        Called when the custom context menu is requested (on right click generally).

        :param pos: The position for the menu
        :type pos: QtCore.QPoint
        """
        menu = QtWidgets.QMenu(self)
        action_promote = QtWidgets.QAction("Promote To...", self)
        action_promote.triggered.connect(self.on_action_promote_selected)
        menu.addAction(action_promote)
        menu.exec_(self.ui.treeView.mapToGlobal(pos))

    def on_action_promote_selected(self):
        """
        Called when the user want to promote a compound.
        """
        self.picker = FormCompoundPicker(self.manager.registry)
        self.picker.onPicked.connect(self._promote_selected)
        self.picker.exec_()

    def _promote_selected(self, compound_definition):
        """
        Called when the user submitted a compound to be promoted.
        :param compound_definition: The compound definition to protomote to
        :type compound_definition: omtk_compound.CompoundDefinition
        """
        compounds = self._get_selected_compounds()
        path = compound_definition["path"]

        for compound in compounds:
            # TODO: Move to shared function
            _LOG.info("Promoting %s to %s", compound, compound_definition)
            namespace = compound.namespace
            connections = compound.hold_connections()
            compound.delete()
            new_compound = from_file(path, namespace=namespace)
            new_compound.fetch_connections(*connections)
