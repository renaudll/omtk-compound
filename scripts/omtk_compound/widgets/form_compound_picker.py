"""
Modal dialog for picking a compound definition from a registry.
"""
from omtk_compound.core import CompoundDefinition
from omtk_compound.vendor.Qt import QtCore, QtWidgets
from omtk_compound.widgets.ui import form_compound_picker as ui_def
from omtk_compound.models import CompoundRegistryModel, DataRole


class FormCompoundPicker(QtWidgets.QDialog):  # pylint: disable=too-few-public-methods
    """
    Form that list registered compound definitions.
    """

    onPicked = QtCore.Signal(CompoundDefinition)

    def __init__(self, registry):
        """
        :param omtk_compound.Registry registry: A compound definition registry
        """
        super(FormCompoundPicker, self).__init__()

        self.ui = ui_def.Ui_Dialog()
        self.ui.setupUi(self)

        self.model = CompoundRegistryModel(registry)
        self.ui.tableView.setModel(self.model)

        self.accepted.connect(self.on_accepted)

    def _get_selected_data(self):
        """
        :return: The selected compound definition
        :rtype: CompoundDefinition
        """
        index = self.ui.tableView.selectionModel().selectedRows()[0]
        return self.model.data(index, DataRole)

    def on_accepted(self):
        """
        Triggered when the user choose a compound definition.
        """
        compound_def = self._get_selected_data()
        self.onPicked.emit(compound_def)
