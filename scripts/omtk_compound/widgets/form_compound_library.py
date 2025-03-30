"""
Window that show the available registered compounds.
"""

from omtk_compound.vendor.Qt import QtCore, QtWidgets
from omtk_compound.core._factory import from_file
from omtk_compound import manager
from omtk_compound.models import CompoundRegistryModel, DataRole

from .ui import form_compound_library as ui_def


class FormCompoundLibrary(QtWidgets.QMainWindow):
    """
    Window that show the available registered compounds.
    """

    def __init__(self) -> None:
        super().__init__()
        self.ui = ui_def.Ui_MainWindow()
        self.ui.setupUi(self)

        self.compound_model = CompoundRegistryModel(manager.registry)
        self.ui.tableView_compounds.setModel(self.compound_model)

        self.ui.tableView_compounds.selectionModel().selectionChanged.connect(
            self.on_selection_changed
        )
        self.ui.pushButton_create.pressed.connect(self.on_submit)
        self.ui.lineEdit_create_namespace.textChanged.connect(self.update_enabled)

        self.update_enabled()

    def update_enabled(self, *_) -> None:
        """
        Update the status of the "create" button.
        """
        text = self.ui.lineEdit_create_namespace.text()
        self.ui.pushButton_create.setEnabled(bool(text))

    def on_submit(self) -> None:
        """
        Called when the user submit is request to create a Compound.
        """
        sel = self.get_selected_compound_def()
        name = self.ui.lineEdit_create_namespace.text()
        from_file(sel.path, namespace=name)

    def on_selection_changed(self, selected: QtCore.QItemSelection, _) -> None:
        """
        Called when the user select a component
        :param selected: Selected items
        """
        if selected.empty():
            return

        compound_def = self.get_selected_compound_def()

        text = (
            f"Name: {compound_def['name']}\n"
            f"Version: {compound_def['version']}\n"
            f"Author: {compound_def['author']}\n"
            f"Description: {compound_def['description']}\n"
        )

        self.ui.plainTextEdit_details.setPlainText(text)

    def get_selected_compound_def(self) -> manager.CompoundDefinition:
        """
        Get the selected compound definition.
        """
        selected = self.ui.tableView_compounds.selectedIndexes()
        index = next((index for index in selected))
        compound_def = self.compound_model.data(index, DataRole)
        return compound_def
