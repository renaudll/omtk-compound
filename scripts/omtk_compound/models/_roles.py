""" Custom Qt roles"""
from omtk_compound.vendor.Qt import QtCore

# Role used to query the model data.
DataRole = QtCore.Qt.UserRole + 1  # pylint: disable=invalid-name
