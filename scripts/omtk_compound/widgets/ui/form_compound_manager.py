# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/dev/py/omtk-compound/scripts/omtk_compound/widgets/ui/form_compound_manager.ui'
#
# Created: Wed Nov 20 23:30:48 2019
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from omtk_compound.vendor.Qt import QtCompat, QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(789, 543)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.widget_outliner = CompoundOutlinerWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_outliner.sizePolicy().hasHeightForWidth())
        self.widget_outliner.setSizePolicy(sizePolicy)
        self.widget_outliner.setObjectName("widget_outliner")
        self.verticalLayout.addWidget(self.widget_outliner)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_editor = CompoundEditorWidget(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_editor.sizePolicy().hasHeightForWidth())
        self.widget_editor.setSizePolicy(sizePolicy)
        self.widget_editor.setObjectName("widget_editor")
        self.horizontalLayout.addWidget(self.widget_editor)
        self.horizontalLayout_2.addWidget(self.groupBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 789, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtCompat.translate("MainWindow", "MainWindow", None, -1))
        self.label.setText(QtCompat.translate("MainWindow", "Outliner", None, -1))
        self.pushButton.setText(QtCompat.translate("MainWindow", "Create", None, -1))
        self.pushButton_2.setText(QtCompat.translate("MainWindow", "Publish", None, -1))
        self.groupBox.setTitle(QtCompat.translate("MainWindow", "Editor", None, -1))

from ..widget_compound_outliner import CompoundOutlinerWidget
from ..widget_compound_editor import CompoundEditorWidget
