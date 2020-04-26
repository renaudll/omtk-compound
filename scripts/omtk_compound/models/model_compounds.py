"""
Model for displaying compounds in a QTableView.
"""
from ..vendor.Qt import QtCore
from ._roles import DataRole
from ._base import BaseTableModel


class CompoundManagerModel(BaseTableModel):
    """
    Model for displaying compounds in a QTableView.
    """

    _COLUMNS = ["namespace", "type", "version", "status"]

    def __init__(self, manager, entries=None):
        """
        :param manager: A manager
        :type manage: omtk_compound.Manager
        :param entries: An optional list of compounds to display
        :type entries: list[omtk_compound.Compound]
        """
        super(CompoundManagerModel, self).__init__(entries)
        self.manager = manager

    def _get_compound_status(self, compound):
        """
        :param omtk_compound.Compound compound: A compound
        :return: A status
        :rtype: str
        """
        # TODO: Move elsewhere
        metadata = compound.get_metadata()

        try:
            uid = metadata["uid"]
            version = metadata["version"]
            stream = self.manager.registry[uid]
        except KeyError:  # unregistered
            return "unregistered"

        if stream.latest.version == version:
            return "latest"

        return "outdated"

    def _update(self, entries):
        """
        Update internal model data.

        :param entries: New compounds
        :type entries: list[omtk_compound.Compound]
        """
        super(CompoundManagerModel, self)._update(entries)
        self.statuses = [self._get_compound_status(entry) for entry in entries]

    def data(self, index, role):
        """
        Re-implement QtCore.QAbstractTableModel.data

        :param index: The data index
        :type index: QtCore.QModelIndex
        :param int role: A Qt role
        :return:
        :rtype: str or None
        """
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            entry = self.entries[row]  # type: Compound
            if column == 0:
                return entry.namespace

            metadata = entry.get_metadata()
            if column == 1:
                return metadata.get("name", "unregistered")
            if column == 2:
                return metadata.get("version", "unregistered")
            if column == 3:
                return self.statuses[row]

        if role == DataRole:
            row = index.row()
            entry = self.entries[row]
            return entry

        return None
