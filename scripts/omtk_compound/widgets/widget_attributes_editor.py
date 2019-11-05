"""
QWidget that show a list of attributes and allow them to be renamed/reordered.
"""
from omtk_compound.vendor.Qt import QtCore, QtWidgets, QtCompat
from omtk_compound.models import ModelAttributes

from .ui import widget_attributes_editor as ui_def


class AttributesEditorWidget(QtWidgets.QWidget):
    """
    QWidget that show a list of attributes and allow them to be renamed/reordered.
    """

    def __init__(self, parent, data=None):
        """
        :param omtk_compound.Compound compound: The compound to publish
        """
        super(AttributesEditorWidget, self).__init__(parent)

        self.ui = ui_def.Ui_Form()
        self.ui.setupUi(self)

        # Configure models
        self.model = ModelAttributes(data)
        self.proxy_model = QtCore.QSortFilterProxyModel(self)
        self.proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.proxy_model.setSourceModel(self.model)
        self.ui.treeView.setModel(self.proxy_model)

        # Configure appearance
        QtCompat.QHeaderView.setSectionResizeMode(
            self.ui.treeView.header(), QtWidgets.QHeaderView.Stretch
        )
        self.ui.treeView.expandAll()

        # Configure drag and drop
        self.ui.treeView.setDragEnabled(True)
        self.ui.treeView.viewport().setAcceptDrops(True)
        self.ui.treeView.setDragDropOverwriteMode(False)

        # Allow the user to re-order columns
        header = self.ui.treeView.header()
        header.setSectionsMovable(True)

        self.ui.treeView.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

        # Connect events
        self.ui.lineEdit_search.textEdited.connect(self._on_search_changed)

    def set_data(self, data):  # type: (list[str]) -> None
        self.model.set_data(data)
        self.ui.treeView.expandAll()

    def _on_search_changed(self, text):  # (type: str) -> None
        """
        Called when the user change the search query.

        :param text: The new search query
        """
        self.proxy_model.setFilterFixedString(text)
