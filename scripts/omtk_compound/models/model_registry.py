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

    def __init__(self, registry) -> None:
        """
        :param registry: A compound registry
        """
        entries = sorted([registry[uid][version] for uid, version in registry])
        super().__init__(entries)
        self.registry = registry

    def data(self, index: QtCore.QModelIndex, role: int) -> str | None:
        """
        :param index: The data index
        :param role: A Qt role
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
