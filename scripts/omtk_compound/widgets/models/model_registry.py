"""
Model for displaying a registered component definitions in a QTableView.
"""
from omtk_compound.core._definition import CompoundDefinition
from omtk_compound.vendor.Qt import QtCore

DataRole = QtCore.Qt.UserRole + 1


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

    def rowCount(self, _):
        return len(self.entries)

    def columnCount(self, _):
        return len(self._COLUMNS)

    def headerData(self, section, orientation, role):
        """
        :param int section:
        :param int orientation:
        :param int role:
        :return:
        """
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return str(self._COLUMNS[section])

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
            return getattr(entry, key) or ''

        if role == DataRole:
            row = index.row()
            return self.entries[row]
