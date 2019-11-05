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

        self.ui = ui_def.Ui_Form()
        self.ui.setupUi(self)

        self.manager = manager
        compounds = tuple(from_scene())
        self.model = CompoundManagerModel(self.manager, entries=compounds)
        self.ui.treeView.setModel(self.model)
        self.selectionModel = self.ui.treeView.selectionModel()

        self.selectionModel.selectionChanged.connect(self.on_selection_changed)
        self.ui.treeView.customContextMenuRequested.connect(
            self.on_custom_context_menu_requested
        )

    def _get_selected_compounds(self):
        """
        :return: A list of selected compounds
        :rtype: List[omtk_compound.Compounds]
        """
        indexes = self.selectionModel.selectedRows()
        return [self.model.data(index, DataRole) for index in indexes]

    def on_selection_changed(self, selected, deselected):
        objs = set()
        compounds = self._get_selected_compounds()
        for compound in compounds:
            objs.update(compound.nodes)
        cmds.select(list(objs))
        self.selectionChanged.emit(compounds)

    def on_custom_context_menu_requested(self, pos):
        menu = QtWidgets.QMenu(self)
        actionPromote = QtWidgets.QAction("Promote To...", self)
        actionPromote.triggered.connect(self.on_action_promote_selected)
        menu.addAction(actionPromote)
        menu.exec_(self.ui.treeView.mapToGlobal(pos))

    def on_action_promote_selected(self):
        self.picker = FormCompoundPicker(self.manager.registry)
        self.picker.onPicked.connect(self._promote_selected)
        self.picker.exec_()

    def _promote_selected(self, compound_definition):
        compounds = self._get_selected_compounds()
        path = compound_definition["path"]

        for compound in compounds:
            # TODO: Move to shared function
            _LOG.info("Promoting %s to %s" % (compound, compound_definition))
            namespace = compound.namespace
            connections = compound.hold_connections()
            compound.delete()
            new_compound = from_file(path, namespace=namespace)
            new_compound.fetch_connections(*connections)
