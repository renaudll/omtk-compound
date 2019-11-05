"""
Window that show the available registered compounds.
"""
import omtk_compound
from omtk_compound.vendor.Qt import QtWidgets
from omtk_compound.core._factory import from_file
from omtk_compound import manager
from omtk_compound.models import CompoundRegistryModel, DataRole

from .ui import form_compound_library as ui_def


class FormCompoundLibrary(QtWidgets.QMainWindow):
    """
    Window that show the available registered compounds.
    """
    def __init__(self):
        super(FormCompoundLibrary, self).__init__()

        self.ui = ui_def.Ui_MainWindow()
        self.ui.setupUi(self)

        self.compound_model = CompoundRegistryModel(manager.registry)
        self.ui.tableView_compounds.setModel(self.compound_model)

        self.ui.tableView_compounds.selectionModel().selectionChanged.connect(
            self.on_selection_changed
        )
        self.ui.pushButton_create.pressed.connect(self.on_submit)
        self.ui.lineEdit_create_namespace.textChanged.connect(self.on_namespace_changed)

        self.update_enabled()

    def update_enabled(self):
        text = self.ui.lineEdit_create_namespace.text()
        self.ui.pushButton_create.setEnabled(bool(text))

    def on_namespace_changed(self, text):
        self.update_enabled()

    def on_submit(self):
        """
        Called when the user submit is request to create a Compound.
        """
        sel = self.get_selected_compound_def()
        name = self.ui.lineEdit_create_namespace.text()
        from_file(sel.path, namespace=name)

    def on_selection_changed(self, selected, deselected):
        """
        Called when the user select a component
        :param selected: Selected items
        :param deselected: Unselected items
        """
        if selected.empty():
            return

        compound_def = self.get_selected_compound_def()

        text = (
            "Name: {name}\n"
            "Version: {version}\n"
            "Author: {author}\n"
            "Description: {description}\n"
        ).format(**compound_def)

        self.ui.plainTextEdit_details.setPlainText(text)

    def get_selected_compound_def(self):
        """
        :param selected: QSelection
        :return:
        :rtype: omtk_compound.CompoundDefinition
        """
        selected = self.ui.tableView_compounds.selectedIndexes()
        index = next((index for index in selected))
        compound_def = self.compound_model.data(
            index, DataRole
        )  # type: omtk_compound.CompoundDefinition
        return compound_def
