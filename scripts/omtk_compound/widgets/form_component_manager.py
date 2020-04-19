"""
Window that contain multiple widgets at once to ease workflow.
This is part of UI experimentation and might disappear eventually.
"""
import logging

from omtk_compound.core._factory import from_scene, from_file
from omtk_compound.vendor.Qt import QtWidgets
from omtk_compound.widgets.ui import form_compound_manager as ui_def
from omtk_compound.widgets.form_compound_picker import FormCompoundPicker

_LOG = logging.getLogger(__name__)

# TODO: CompoundListener

_GUI_CREATE = None


class FormCompoundManager(QtWidgets.QMainWindow):
    """
    A form that contain multiple compound related widgets.
    """

    def __init__(self, manager):
        """
        :param omtk_compound.Manager manager: A manager instance
        """
        super(FormCompoundManager, self).__init__()

        self.ui = ui_def.Ui_MainWindow()
        self.ui.setupUi(self)

        self.manager = manager

        self.compounds = tuple(from_scene())
        self.compound = next(iter(self.compounds), None)

        # Configure outliner
        self.ui.widget_outliner.selectionChanged.connect(
            self.on_outliner_selection_changed
        )

        # Configure editor
        self.ui.widget_editor.set_compound(self.compound)

        self.ui.pushButton.pressed.connect(self.show_create)
        self.ui.pushButton_2.pressed.connect(self.show_publisher)

    def on_outliner_selection_changed(self, compounds):
        """
        Called when the user change the selection in the outliner.
        """
        compound = next(iter(compounds), None)
        self.ui.widget_editor.set_compound(compound)

    def show_create(self):
        """
        Show a modal compound picker.
        """
        # workaround maya garbage collection
        global _GUI_CREATE  # pylint: disable=global-statement
        _GUI_CREATE = FormCompoundPicker(self.manager.registry)
        _GUI_CREATE.onPicked.connect(self.on_show_create_picked)
        _GUI_CREATE.show()

    @staticmethod
    def on_show_create_picked(component_def):
        """
        :param component_def: The compound definition to instanciante
        :type component_def: omtk_compound.CompoundDefinition
        """
        from_file(component_def.path)

    @staticmethod
    def show_publisher():
        """
        Show the compound publisher.
        """
        from omtk_compound import macros  # pylint: disable=cyclic-import

        macros.show_form_publish_compound()
