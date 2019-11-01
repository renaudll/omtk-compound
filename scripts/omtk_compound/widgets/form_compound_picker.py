"""
Modal dialog for picking a compound definition from a registry.
"""
from omtk_compound.core import CompoundDefinition
from omtk_compound.vendor.Qt import QtCore, QtWidgets
from omtk_compound.widgets.ui import form_compound_picker as ui_def
from omtk_compound.widgets.models.model_registry import CompoundRegistryModel, DataRole


class FormComponentPicker(QtWidgets.QDialog):
    onPicked = QtCore.Signal(CompoundDefinition)

    def __init__(self, registry):
        """
        :param omtk_compound.Registry registry: A compound definition registry
        """
        super(FormComponentPicker, self).__init__()

        self.ui = ui_def.Ui_Dialog()
        self.ui.setupUi(self)

        self.model = CompoundRegistryModel(registry)
        self.ui.tableView.setModel(self.model)

        self.accepted.connect(self.on_accepted)

    def _get_selected_data(self):
        index = self.ui.tableView.selectionModel().selectedRows()[0]
        return self.model.data(index, DataRole)  # type: CompoundDefinition

    def on_accepted(self):
        """
        Triggered when the user choose a compound definition.
        """
        compound_def = self._get_selected_data()
        self.onPicked.emit(compound_def)
