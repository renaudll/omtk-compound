"""
Model for displaying a registered component definitions in a QTableView.
"""
from omtk_compound.core._definition import CompoundDefinition
from omtk_compound.vendor.Qt import QtCore
from omtk_compound.models._roles import DataRole


class CompoundRegistryModel(QtCore.QAbstractTableModel):
    """
    Model for displaying a registered component definitions in a QTableView.
    """

    _COLUMNS = ("name", "version", "author")
    compoundChoosed = QtCore.Signal(CompoundDefinition)

    def __init__(self, registry):
        """
        :param Registry registry: A compound registry
        """
        super(CompoundRegistryModel, self).__init__()
        self.registry = registry
        self.entries = sorted([registry[uid][version] for uid, version in registry])

    def rowCount(self, _):  # pylint: disable=invalid-name
        """
        Re-implement QtCore.QAbstractTableModel.rowCount

        :return: The number of rows
        :rtype: int
        """
        return len(self.entries)

    def columnCount(self, _):  # pylint: disable=invalid-name
        """
        Re-implement QtCore.QAbstractTableModel.columnCount

        :return: The number of columns
        :rtype: int
        """
        return len(self._COLUMNS)

    def headerData(self, section, orientation, role):  # pylint: disable=invalid-name
        """
        Re-implement QtCore.QAbstractTableModel.headerData

        :param int section: The header section
        :param int orientation: The header orientation
        :param int role: The data role
        :return:
        :rtype: str or None
        """
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return str(self._COLUMNS[section])

        return None

    def data(self, index, role):
        """
        :param index: The data index
        :type index: QtCore.QModelIndex
        :param int role: A Qt role
        :return:
        """
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            entry = self.entries[row]  # type: CompoundDefinition
            key = self._COLUMNS[column]
            return getattr(entry, key) or ""

        if role == DataRole:
            row = index.row()
            return self.entries[row]

        return None
