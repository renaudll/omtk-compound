# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/dev/py/omtk-compound/scripts/omtk_compound/widgets/ui/form_compound_library.ui'
#
# Created: Sat Nov 16 20:11:31 2019
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from omtk_compound.vendor.Qt import QtCompat, QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(572, 534)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit_compounds_search = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_compounds_search.setObjectName("lineEdit_compounds_search")
        self.verticalLayout.addWidget(self.lineEdit_compounds_search)
        self.tableView_compounds = QtWidgets.QTableView(self.centralwidget)
        self.tableView_compounds.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        self.tableView_compounds.setObjectName("tableView_compounds")
        self.verticalLayout.addWidget(self.tableView_compounds)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_description = QtWidgets.QLabel(self.centralwidget)
        self.label_description.setObjectName("label_description")
        self.verticalLayout_3.addWidget(self.label_description)
        self.plainTextEdit_details = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_details.setReadOnly(True)
        self.plainTextEdit_details.setObjectName("plainTextEdit_details")
        self.verticalLayout_3.addWidget(self.plainTextEdit_details)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_create = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_create.setObjectName("pushButton_create")
        self.horizontalLayout_2.addWidget(self.pushButton_create)
        self.lineEdit_create_namespace = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_create_namespace.setObjectName("lineEdit_create_namespace")
        self.horizontalLayout_2.addWidget(self.lineEdit_create_namespace)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 572, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QtCompat.translate("MainWindow", "Compound Library", None, -1)
        )
        self.label_description.setText(
            QtCompat.translate("MainWindow", "Description", None, -1)
        )
        self.pushButton_create.setText(
            QtCompat.translate("MainWindow", "Create", None, -1)
        )
        self.lineEdit_create_namespace.setText(
            QtCompat.translate("MainWindow", "compound", None, -1)
        )
