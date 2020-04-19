"""
Widget that display the input and output attributes of a compound.
"""
from omtk_compound.vendor.Qt import QtWidgets

from .ui import widget_compound_editor as ui_def


class CompoundEditorWidget(QtWidgets.QWidget):  # pylint: disable=too-few-public-methods
    """
    Widget that display the input and output attributes of a compound.
    """

    def __init__(self, parent, compound=None):
        """
        :param omtk_compound.Compound compound: The compound to publish
        """
        super(CompoundEditorWidget, self).__init__(parent)

        self._compound = compound

        self.ui = ui_def.Ui_Form()
        self.ui.setupUi(self)

        self.set_compound(compound)

    def set_compound(self, compound):
        """
        Set the current compound to display

        :param omtk_compound.Compound compound: A compound
        """
        self.ui.widget_inputs.set_data(compound.inputs if compound else None)
        self.ui.widget_outputs.set_data(compound.outputs if compound else None)
