"""
Model for displaying compounds in a QTableView.
"""
from maya import cmds

from omtk_compound import Compound
from omtk_compound.vendor.Qt import QtCore


class AbstractModelCompoundBound(QtCore.QAbstractTableModel):
    _COMPOUND_NODE = "input"
    _COMPOUND_ATTRS = "inputs"
    _COLUMNS = ["name", "type", "multi"]

    def __init__(self, compound):  # type: (Compound) -> None
        super(AbstractModelCompoundBound, self).__init__()
        self.compound = compound

    @property
    def node(self):  # type: () -> str
        """
        :return: The dagpath of the inspected compound node.
        """
        return getattr(self.compound, self._COMPOUND_NODE)

    @property
    def attributes(self):  # type: () -> list[str]
        """
        :return: The list of attributes of defined compound node.
        """
        return sorted(getattr(self.compound, self._COMPOUND_ATTRS))

    def rowCount(self, _):  # type: (QtCore.QModelIndex) -> int
        """ Implement `QtCore.QAbstractItemModel.rowCount`
        """
        return len(self.attributes)

    def columnCount(self, _):  # type: (QtCore.QModelIndex) -> int
        """ Implement `QtCore.QAbstractItemModel.rowCount`
        """
        return len(self._COLUMNS)

    def headerData(self, section, orientation, role):  # type: (int, int, int) -> str
        """ Implement `QtCore.QAbstractItemModel.headerData`
        """
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return str(self._COLUMNS[section])

    def data(self, index, role):  # type: (QtCore.QModelIndex, int) -> object
        """ Implement `QtCore.QAbstractItemModel.data`
        """
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()

            attr_name = self.attributes[row].split('.', 1)[1]
            if column == 0:  # name
                return attr_name
            if column == 1:  # type
                return "not implemented"
            if column == 2:  # multi?
                return "not implemented"

    def setData(self, index, value, role):  # type: (QtCore.QModelIndex, str, int) -> None
        """ Implement `QtCore.QAbstractItemModel.setData
        """
        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            row = index.row()
            src_attr_path = self.attributes[row]

            # Validate the attribute is available
            dst_attr_path = ".".join((self.node, value))
            if cmds.objExists(dst_attr_path):
                cmds.warning("Attribute %r already exist." % dst_attr_path)
                return

            cmds.renameAttr(src_attr_path, value)


class ModelCompoundInputs(AbstractModelCompoundBound):
    """
    Model for displaying and editing a component input attributes.
    """

    _COMPOUND_NODE = "input"
    _COMPOUND_ATTRS = "inputs"


class ModelCompoundOutputs(AbstractModelCompoundBound):
    """
    Model for displaying and editing a component output attributes.
    """

    _COMPOUND_NODE = "output"
    _COMPOUND_ATTRS = "outputs"
