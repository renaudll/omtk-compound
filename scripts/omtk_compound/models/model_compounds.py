"""
Model for displaying compounds in a QTableView.
"""
from omtk_compound.vendor.Qt import QtCore
from omtk_compound.models._roles import DataRole


class CompoundManagerModel(QtCore.QAbstractTableModel):
    """
    Model for displaying compounds in a QTableView.
    """
    _COLUMNS = ["namespace", "type", "version", "status"]

    def __init__(self, manager, entries=None):
        super(CompoundManagerModel, self).__init__()
        self.manager = manager
        self._update(entries or [])

    def _get_compound_status(self, compound):
        """
        :param Compound compound:
        :return:
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
        else:
            return "outdated"

    def _update(self, entries):
        self.entries = entries
        self.statuses = [self._get_compound_status(entry) for entry in entries]

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
