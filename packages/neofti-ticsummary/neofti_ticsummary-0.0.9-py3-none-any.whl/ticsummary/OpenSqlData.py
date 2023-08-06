from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox


class Ui_OpenSQLDataDialog(object):
    def setupUi(self, OpenSQLDataDialog):
        OpenSQLDataDialog.setObjectName("OpenSQLDataDialog")
        OpenSQLDataDialog.resize(701, 600)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(OpenSQLDataDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButtonSeveral = QtWidgets.QRadioButton(OpenSQLDataDialog)
        self.radioButtonSeveral.setChecked(True)
        self.radioButtonSeveral.setObjectName("radioButtonSeveral")
        self.verticalLayout.addWidget(self.radioButtonSeveral)
        self.radioButtonFromFirst = QtWidgets.QRadioButton(OpenSQLDataDialog)
        self.radioButtonFromFirst.setObjectName("radioButtonFromFirst")
        self.verticalLayout.addWidget(self.radioButtonFromFirst)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.tableViewData = QtWidgets.QTableView(OpenSQLDataDialog)
        self.tableViewData.setObjectName("tableViewData")
        self.verticalLayout_2.addWidget(self.tableViewData)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonOpen = QtWidgets.QPushButton(OpenSQLDataDialog)
        self.pushButtonOpen.setObjectName("pushButtonOpen")
        self.horizontalLayout.addWidget(self.pushButtonOpen)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(OpenSQLDataDialog)
        QtCore.QMetaObject.connectSlotsByName(OpenSQLDataDialog)

    def retranslateUi(self, OpenSQLDataDialog):
        _translate = QtCore.QCoreApplication.translate
        OpenSQLDataDialog.setWindowTitle(_translate("OpenSQLDataDialog", "Open data"))
        self.radioButtonSeveral.setText(_translate("OpenSQLDataDialog", "Selection of several data"))
        self.radioButtonFromFirst.setText(_translate("OpenSQLDataDialog", "Selection of several from the first"))
        self.pushButtonOpen.setText(_translate("OpenSQLDataDialog", "Open"))



class OpenSQLData():
    def __init__(self, model, funcCallback):
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_OpenSQLDataDialog()
        self.ui.setupUi(self.dialog)
        self.model = model
        
        self.ui.tableViewData.setModel(self.model)
        self.ui.tableViewData.setSelectionModel(QtWidgets.QAbstractItemView.SelectionMode.ContiguousSelection)
        
        self.ui.radioButtonSeveral.toggled.connect(self.radioButtonSeveralToggled)
        self.ui.radioButtonFromFirst.toggled.connect(self.radioButtonFromFirstToggled)
        self.ui.pushButtonOpen.clicked.connect(self.pushButtonOpenClicked)
        self.funcCallBack = funcCallback
    def show(self):
        self.dialog.show()
    
    def radioButtonSeveralToggled(self, checked:bool):
        if checked:
            self.ui.tableViewData.setSelectionModel(QtWidgets.QAbstractItemView.SelectionMode.ContiguousSelection)
            self.ui.tableViewData.clearSelection()
    def radioButtonFromFirstToggled(self, checked:bool):
        if checked:
            self.ui.tableViewData.setSelectionModel(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
            self.ui.tableViewData.clearSelection()
    def pushButtonOpenClicked(self):
        list = self.ui.tableViewData.selectionModel().selectedRows()
        
        if list.count() <= 0:
            msqBox = QMessageBox()
            msqBox.setText("No data selected. \nPlease select data")
            msqBox.exec()
            return;
        if self.ui.radioButtonSeveral.isChecked():
            self.selectedRow = list
        if self.ui.radioButtonFromFirst.isChecked():
            for i in range(list[0]+1, self.ui.tableViewData.model().rowCount()):
                list.append(i)
            self.selectedRow = list
            self.funcCallBack(list)
        
        
    