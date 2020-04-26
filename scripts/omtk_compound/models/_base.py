"""
Base model classes
"""
from ..vendor.Qt import QtCore


class BaseTableModel(QtCore.QAbstractTableModel):
    """
    Intermediate QAbstractTableModel implementation
    """

    _COLUMNS = []

    def __init__(self, entries=None):
        """
        :param entries: An optional list of compounds to display
        :type entries: list[omtk_compound.Compound]
        """
        super(BaseTableModel, self).__init__()
        self._update(entries or [])

    def _update(self, entries):
        """
        Update internal model data.

        :param entries: New compounds
        :type entries: list[omtk_compound.Compound]
        """
        self.entries = entries

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
