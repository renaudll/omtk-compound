"""
Base model classes
"""

from ..core._compound import Compound
from ..vendor.Qt import QtCore


class BaseTableModel(QtCore.QAbstractTableModel):
    """
    Intermediate QAbstractTableModel implementation
    """

    _COLUMNS: list[str] = []

    def __init__(self, entries: list[Compound] | None = None) -> None:
        """
        :param entries: An optional list of compounds to display
        """
        super().__init__()
        self._update(entries or [])

    def _update(self, entries: list[Compound]) -> None:
        """
        Update internal model data.

        :param entries: New compounds
        """
        self.entries = entries

    def rowCount(self, _) -> int:
        """
        Re-implement QtCore.QAbstractTableModel.rowCount

        :return: The number of rows
        """
        return len(self.entries)

    def columnCount(self, _) -> int:
        """
        Re-implement QtCore.QAbstractTableModel.columnCount

        :return: The number of columns
        """
        return len(self._COLUMNS)

    def headerData(self, section: int, orientation: int, role: int) -> str | None:
        """
        Re-implement QtCore.QAbstractTableModel.headerData

        :param section: The header section
        :param orientation: The header orientation
        :param role: The data role
        """
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return f"{self._COLUMNS[section]}"
        return None
