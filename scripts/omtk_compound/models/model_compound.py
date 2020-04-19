"""
Model for displaying compounds in a QTableView.
"""
import logging
import itertools
from maya import cmds

from omtk_compound.models._roles import DataRole
from omtk_compound.core._utils_attr import reorder_attributes
from omtk_compound.vendor.Qt import QtCore, QtGui


_LOG = logging.getLogger(__name__)


class ModelAttributes(QtGui.QStandardItemModel):
    """
    Model that display a list of attributes.
    """

    _COLUMNS = ["name", "type", "multi"]

    def __init__(self, attributes=None):
        """
        :param attributes: An optional list of attributes.
        :type attributes: list[str]
        """
        super(ModelAttributes, self).__init__()

        self.setColumnCount(len(self._COLUMNS))
        self.setHorizontalHeaderLabels(self._COLUMNS)

        self.set_data(attributes)

    def removeRows(self, *args, **kwargs):  # pylint: disable=invalid-name
        """
        Re-implement QtGui.QStandardItemModel.removeRows

        :param args: Any position arguments are forwarded to the parent implementation.
        :param kwargs: Any keyword arguments are forwarded to the parent implementation.
        :return: Where the rows removed?
        :rtype: bool
        """
        # Hack: When doing a drag and drop in Qt,
        # it call insertRows followed by removeRows.
        # There's indication that could call moveRows,
        # but there seem to be no point of entry for it.
        # https://stackoverflow.com/questions/40347852/qt-qabstractitemmodel-dragdrop-for-moving-items-performs-remove-insert
        # So we'll *wrongly* assume removeRows mean the attributes have been re-ordered.
        try:
            return super(ModelAttributes, self).removeRows(*args, **kwargs)
        finally:
            self.__reorder()

    def __reorder(self):
        """Apply new ordering to maya attributes."""
        root = self.invisibleRootItem()
        attributes = [root.child(row).data(DataRole) for row in range(root.rowCount())]

        node = attributes[0].split(".")[0]
        attribute_names = [attr.split(".")[-1] for attr in attributes]
        _LOG.info("Reordering attributes: %s, %s", node, attribute_names)
        reorder_attributes(node, attribute_names)

    def set_data(self, attributes):  # TODO: Rename
        """
        Set the model internal data

        :param attributes: The attributes to show
        :type attributes: list[str]
        """
        self.beginResetModel()
        if attributes:
            self.__update(attributes)
        self.endResetModel()

    def __update(self, attributes):  # pylint: disable=too-many-locals
        """
        Build the internal tree.

        :param attributes: A list of attributes.
        :return: The tree root item.
        """
        root = self.invisibleRootItem()
        root.setDragEnabled(False)

        # Note: sorted will put None first
        attributes_by_parent = itertools.groupby(
            sorted(attributes, key=_get_attribute_parent), _get_attribute_parent
        )

        item_by_attr = {}
        for parent_attr, attributes_ in attributes_by_parent:
            attributes_ = tuple(attributes)

            for attribute in attributes_:

                # Get data from attribute
                parent = item_by_attr.get(parent_attr, root)
                node_name, attr_name = attribute.split(".", 1)
                attr_type = cmds.getAttr(attribute, type=True)
                attr_multi = cmds.attributeQuery(attr_name, node=node_name, multi=True)

                item1 = QtGui.QStandardItem(attr_name)
                item1.setData(attribute, DataRole)
                item2 = QtGui.QStandardItem(attr_type)
                item3 = QtGui.QStandardItem(str(attr_multi))

                # Prevent item overwrite with a drop
                item1.setDropEnabled(False)
                item2.setDropEnabled(False)
                item3.setDropEnabled(False)

                # Prevent re-ordering of child attributes
                if parent is not root:
                    item1.setDragEnabled(False)
                    item2.setDragEnabled(False)
                    item3.setDragEnabled(False)

                parent.appendRow([item1, item2, item3])
                item_by_attr[attribute] = item1

    @staticmethod
    def supportedDropActions():  # pylint: disable=invalid-name
        """
        Re-implement QtCore.QAbstractItemModel.supportedDropActions

        :return: The supported drop actions
        :rtype: int
        """
        return QtCore.Qt.MoveAction

    def setData(self, index, value, role):  # pylint: disable=invalid-name
        """
        Implement `QtCore.QAbstractItemModel.setData

        :param QtCore.QModelIndex index: The index to set
        :param str value: The value to set
        :param int role: The set role
        :return: True if the set was successful
        :rtype: bool
        """
        if role != QtCore.Qt.EditRole:
            return False

        item = self.itemFromIndex(index)

        src_attr_path = index.data(DataRole)  # type: str
        node = src_attr_path.split(".")[0]
        dst_attr_path = ".".join((node, value))

        # Validate the attribute is available
        if cmds.objExists(dst_attr_path):
            cmds.warning("Attribute %r already exist." % str(dst_attr_path))
            return False

        cmds.renameAttr(src_attr_path, value)

        # Update internal data
        item.setText(value)
        item.setData(dst_attr_path, DataRole)

        self.dataChanged.emit(index, index)
        return True


def _get_attribute_parent(attr):  # type: (str) -> str
    """ Utility method that return an attribute parent.
    """
    node_name, attr_name = attr.split(".", 1)
    parents = cmds.attributeQuery(attr_name, node=node_name, listParent=True)
    return ".".join((node_name, parents[0])) if parents else None
