# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/dev/py/omtk-compound/scripts/omtk_compound/widgets/ui/widget_compound_editor.ui'
#
# Created: Thu Nov 21 22:03:29 2019
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from omtk_compound.vendor.Qt import QtCompat, QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_inputs = AttributesEditorWidget(Form)
        self.widget_inputs.setObjectName("widget_inputs")
        self.horizontalLayout.addWidget(self.widget_inputs)
        self.widget_outputs = AttributesEditorWidget(Form)
        self.widget_outputs.setObjectName("widget_outputs")
        self.horizontalLayout.addWidget(self.widget_outputs)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtCompat.translate("Form", "Form", None, -1))


from ..widget_attributes_editor import AttributesEditorWidget
