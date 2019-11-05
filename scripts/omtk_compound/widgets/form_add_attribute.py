""" Helper UI to create Compound. """
import logging

import pymel.core as pymel
from maya import cmds

from omtk_compound.vendor.Qt import QtWidgets
from omtk_compound.widgets.ui import form_add_attribute as ui_def

_LOG = logging.getLogger(__name__)

# maya known attr type names
_TYPE_FLOAT = "float"
_TYPE_INT = "byte"  # 8 bit integer
_TYPE_STR = "string"
_TYPE_BOOL = "bool"
_TYPE_MATRIX = "matrix"
_TYPE_MESSAGE = "message"
_KWARG_MAP = {
    "bool": {"at": "double"},
    "long": {"at": "long"},
    "short": {"at": "short"},
    "byte": {"at": "byte"},
    "char": {"at": "char"},
    "enum": {"at": "enum"},
    "float": {"at": "float"},
    "double": {"at": "double"},
    "doubleAngle": {"at": "doubleAngle"},
    "doubleLinear": {"at": "doubleLinear"},
    "string": {"dt": "string"},
    "stringArray": {"dt": "stringArray"},
    "compound": {"at": "compound"},
    "message": {"at": "message"},
    "time": {"at": "time"},
    "matrix": {"dt": "matrix"},
    "fltMatrix": {"at": "fltMatrix"},
    "reflectanceRGB": {"dt": "reflectanceRGB"},
    "reflectance": {"at": "reflectance"},
    "spectrumRGB": {"dt": "spectrumRGB"},
    "spectrum": {"at": "spectrum"},
    "float2": {"dt": "float2"},
    "float3": {"dt": "float3"},
    "double2": {"dt": "double2"},
    "double3": {"dt": "double3"},
    "long2": {"dt": "long2"},
    "long3": {"dt": "long3"},
    "short2": {"dt": "short2"},
    "short3": {"dt": "short3"},
    "doubleArray": {"dt": "doubleArray"},
    "Int32Array": {"dt": "Int32Array"},
    "vectorArray": {"dt": "vectorArray"},
    "nurbsCurve": {"dt": "nurbsCurve"},
    "nurbsSurface": {"dt": "nurbsSurface"},
    "mesh": {"dt": "mesh"},
    "lattice": {"dt": "lattice"},
    "pointArray": {"dt": "pointArray"},
}


class FormCreateAttribute(QtWidgets.QMainWindow):
    def __init__(self):
        super(FormCreateAttribute, self).__init__()

        self.ui = ui_def.Ui_MainWindow()
        self.ui.setupUi(self)

        # Set default radio button
        self.ui.rb_float.setChecked(True)

        self.ui.pushButton.pressed.connect(self.on_submit)

    def get_attr_type(self):
        """ Return the attribute type to create

        :return: An attribute type (ex: "string")
        :rtype: str
        """
        if self.ui.rb_float.isChecked():
            return _TYPE_FLOAT
        if self.ui.rb_integer.isChecked():
            return _TYPE_INT
        if self.ui.rb_string.isChecked():
            return _TYPE_STR
        if self.ui.rb_boolean.isChecked():
            return _TYPE_BOOL
        if self.ui.rb_matrix.isChecked():
            return _TYPE_MATRIX
        if self.ui.rb_message.isChecked():
            return _TYPE_MESSAGE
        raise Exception("No attribute type provided")

    @staticmethod
    def add_attribute(obj, name, type_, value):
        """ Add an attribute

        :param str obj: Dagpath of the attribute holder
        :param str name: Attribute name
        :param str type_: Attribute type
        :param str value: Attribute value
        """
        kwargs = _KWARG_MAP[type]  # todo: create method?
        kwargs["longName"] = name
        _LOG.info("Adding attribute %r on %r: %r" % name, obj, kwargs)
        cmds.addAttr(obj, **kwargs)
        attr = "%s.%s" % (obj, name)
        cmds.setAttr(attr, value, type=type_)

    def on_submit(self):
        """ Called when the user pressed submit.
        """
        name = self.ui.lineEdit_name.text()
        type_ = self.get_attr_type()
        value = self.ui.lineEdit_value.text()

        for obj in pymel.selected():
            self.add_attribute(obj, name, type_, value)
