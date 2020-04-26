"""
Model for displaying a registered component definitions in a QTableView.
"""
from ..core._definition import CompoundDefinition
from ..vendor.Qt import QtCore
from ._roles import DataRole
from ._base import BaseTableModel


class CompoundRegistryModel(BaseTableModel):
    """
    Model for displaying a registered component definitions in a QTableView.
    """

    _COLUMNS = ("name", "version", "author")
    compoundChoosed = QtCore.Signal(CompoundDefinition)

    def __init__(self, registry):
        """
        :param Registry registry: A compound registry
        """
        entries = sorted([registry[uid][version] for uid, version in registry])
        super(CompoundRegistryModel, self).__init__(entries)
        self.registry = registry

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
