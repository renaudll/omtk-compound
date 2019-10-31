"""
Helper UI to create "Component".
"""
import uuid

from omtk_compound.core import CompoundDefinition
from omtk_compound.vendor.Qt import QtWidgets
from omtk_compound import manager

from .ui import form_publish_compound as ui_def


class FormPublishCompound(QtWidgets.QMainWindow):
    def __init__(self, compound):
        """
        :param omtk_compound.Compound compound: The compound to publish
        """
        super(FormPublishCompound, self).__init__()

        self._compound = compound

        self.ui = ui_def.Ui_MainWindow()
        self.ui.setupUi(self)

        self.load_compound(compound)

        self.ui.pushButton_submit.pressed.connect(self.on_submit)

    def load_compound(self, compound):
        """
        :param omtk_compound.Compound compound: The compound to load
        """
        metadata = compound.get_metadata()

        self.ui.lineEdit_name.setText(metadata.get("name"))
        self.ui.lineEdit_author.setText(
            metadata.get("author") or manager.preferences.default_author
        )
        self.ui.lineEdit_version.setText(metadata.get("version") or "0.0.1")
        self.ui.lineEdit_uid.setText(metadata.get("uid") or str(uuid.uuid4()))

    def get_definition(self):
        """
        :return: A compound definition using the values in the UI
        :rtype: CompoundDefinition
        """
        name = self.ui.lineEdit_name.text()
        author = self.ui.lineEdit_author.text()
        version = self.ui.lineEdit_version.text()
        uid = self.ui.lineEdit_uid.text()
        return CompoundDefinition(name=name, author=author, version=version, uid=uid)

    def on_submit(self):
        compound = self._compound
        compound_def = self.get_definition()

        compound.set_metadata(compound_def)
        manager.publish_compound(compound)

        self.close()
