from ..core import Compound
from omtk_compound.vendor.Qt import QtWidgets
from .ui import widget_compound_editor as ui_def


class CompoundEditorWidget(QtWidgets.QWidget):  # pylint: disable=too-few-public-methods
    """
    Widget that display the input and output attributes of a compound.
    """

    def __init__(self, parent, compound: Compound = None) -> None:
        """
        :param compound: The compound to publish
        """
        super().__init__(parent)

        self._compound = compound

        self.ui = ui_def.Ui_Form()
        self.ui.setupUi(self)

        self.set_compound(compound)

    def set_compound(self, compound: Compound) -> None:
        """
        Set the current compound to display

        :param compound: A compound
        """
        self.ui.widget_inputs.set_data(compound.inputs if compound else None)
        self.ui.widget_outputs.set_data(compound.outputs if compound else None)
