# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/dev/py/omtk-compound/scripts/omtk_compound/widgets/ui/widget_attribute_tree.ui'
#
# Created: Thu Nov 21 21:50:24 2019
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from omtk_compound.vendor.Qt import QtCompat, QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(320, 284)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit_search = QtWidgets.QLineEdit(Form)
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.verticalLayout.addWidget(self.lineEdit_search)
        self.treeView = QtWidgets.QTreeView(Form)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtCompat.translate("Form", "Form", None, -1))
