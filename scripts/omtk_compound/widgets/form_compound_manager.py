"""
Helper UI to create "Component".
"""
import logging

from maya import cmds

from omtk_compound.core._factory import from_scene, from_file
from omtk_compound.vendor.Qt import QtCore, QtGui, QtWidgets
from omtk_compound.widgets.ui import form_compound_manager as ui_def
from omtk_compound.widgets.models.model_compounds import CompoundManagerModel, QDataRole
from omtk_compound.widgets.form_compound_picker import FormComponentPicker

_LOG = logging.getLogger(__name__)


class FormCompoundManager(QtWidgets.QMainWindow):
    def __init__(self, manager):
        """
        :param omtk_compound.Manager manager: A manager instance
        """
        super(FormCompoundManager, self).__init__()

        self.ui = ui_def.Ui_MainWindow()
        self.ui.setupUi(self)

        self.manager = manager
        compounds = tuple(from_scene())
        self.model = CompoundManagerModel(self.manager, entries=compounds)
        self.ui.tableView.setModel(self.model)
        self.selectionModel = self.ui.tableView.selectionModel()

        self.selectionModel.selectionChanged.connect(self.on_selection_changed)
        self.ui.tableView.customContextMenuRequested.connect(
            self.on_custom_context_menu_requested
        )

    def _get_selected_compounds(self):
        """
        :return: A list of selected compounds
        :rtype: List[omtk_compound.Compounds]
        """
        indexes = self.selectionModel.selectedRows()
        return [self.model.data(index, QDataRole) for index in indexes]

    def on_selection_changed(self, selected, deselected):
        objs = set()
        compounds = self._get_selected_compounds()
        for compound in compounds:
            objs.update(compound.nodes)
        cmds.select(list(objs))

    def on_custom_context_menu_requested(self, pos):
        menu = QtWidgets.QMenu(self)
        actionPromote = QtWidgets.QAction("Promote To...", self)
        actionPromote.triggered.connect(self.on_action_promote_selected)
        menu.addAction(actionPromote)
        menu.exec_(self.ui.tableView.mapToGlobal(pos))

    def on_action_promote_selected(self):
        self.picker = FormComponentPicker(self.manager.registry)
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
