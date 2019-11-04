"""
Helper UI to create "Component".
"""
from omtk_compound.vendor.Qt import QtWidgets
from omtk_compound.widgets.models.model_compound import ModelCompoundInputs, ModelCompoundOutputs

from .ui import form_compound_editor as ui_def


class FormCompoundEditor(QtWidgets.QMainWindow):
    def __init__(self, compound):
        """
        :param omtk_compound.Compound compound: The compound to publish
        """
        super(FormCompoundEditor, self).__init__()

        self._compound = compound

        self.ui = ui_def.Ui_MainWindow()
        self.ui.setupUi(self)

        model_inputs = ModelCompoundInputs(compound)
        model_outputs = ModelCompoundOutputs(compound)
        self.ui.tableViewInputs.setModel(model_inputs)
        self.ui.tableViewOutputs.setModel(model_outputs)

