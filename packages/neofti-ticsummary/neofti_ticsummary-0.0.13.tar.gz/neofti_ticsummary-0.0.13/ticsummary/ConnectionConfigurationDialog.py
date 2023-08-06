from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot 
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from ticsummary import DatabaseMYSQL
import json
import os
from pathlib import Path


class Ui_ConnectionConfigurationDialog(object):
    def setupUi(self, ConnectionConfigurationDialog):
        ConnectionConfigurationDialog.setObjectName("ConnectionConfigurationDialog")
        ConnectionConfigurationDialog.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        ConnectionConfigurationDialog.resize(488, 300)
        ConnectionConfigurationDialog.setModal(True)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(ConnectionConfigurationDialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(ConnectionConfigurationDialog)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(ConnectionConfigurationDialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(ConnectionConfigurationDialog)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(ConnectionConfigurationDialog)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(ConnectionConfigurationDialog)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(ConnectionConfigurationDialog)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEditHost = QtWidgets.QLineEdit(ConnectionConfigurationDialog)
        self.lineEditHost.setObjectName("lineEditHost")
        self.verticalLayout.addWidget(self.lineEditHost)
        self.lineEditDB = QtWidgets.QLineEdit(ConnectionConfigurationDialog)
        self.lineEditDB.setObjectName("lineEditDB")
        self.verticalLayout.addWidget(self.lineEditDB)
        self.spinBoxPort = QtWidgets.QSpinBox(ConnectionConfigurationDialog)
        self.spinBoxPort.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBoxPort.setMaximum(9999)
        self.spinBoxPort.setObjectName("spinBoxPort")
        self.verticalLayout.addWidget(self.spinBoxPort)
        self.lineEditUser = QtWidgets.QLineEdit(ConnectionConfigurationDialog)
        self.lineEditUser.setObjectName("lineEditUser")
        self.verticalLayout.addWidget(self.lineEditUser)
        self.lineEditPassword = QtWidgets.QLineEdit(ConnectionConfigurationDialog)
        self.lineEditPassword.setObjectName("lineEditPassword")
        self.verticalLayout.addWidget(self.lineEditPassword)
        self.lineEditTable = QtWidgets.QLineEdit(ConnectionConfigurationDialog)
        self.lineEditTable.setObjectName("lineEditTable")
        self.verticalLayout.addWidget(self.lineEditTable)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonWriteConf = QtWidgets.QPushButton(ConnectionConfigurationDialog)
        self.pushButtonWriteConf.setObjectName("pushButtonWriteConf")
        self.horizontalLayout.addWidget(self.pushButtonWriteConf)
        self.pushButtonReadConf = QtWidgets.QPushButton(ConnectionConfigurationDialog)
        self.pushButtonReadConf.setObjectName("pushButtonReadConf")
        self.horizontalLayout.addWidget(self.pushButtonReadConf)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButtonSave = QtWidgets.QPushButton(ConnectionConfigurationDialog)
        self.pushButtonSave.setObjectName("pushButtonSave")
        self.horizontalLayout_2.addWidget(self.pushButtonSave)
        self.pushButtonCancel = QtWidgets.QPushButton(ConnectionConfigurationDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout_2.addWidget(self.pushButtonCancel)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.retranslateUi(ConnectionConfigurationDialog)
        QtCore.QMetaObject.connectSlotsByName(ConnectionConfigurationDialog)

    def retranslateUi(self, ConnectionConfigurationDialog):
        _translate = QtCore.QCoreApplication.translate
        ConnectionConfigurationDialog.setWindowTitle(_translate("ConnectionConfigurationDialog", "Connection configuration"))
        self.label.setText(_translate("ConnectionConfigurationDialog", "Host"))
        self.label_2.setText(_translate("ConnectionConfigurationDialog", "Database"))
        self.label_3.setText(_translate("ConnectionConfigurationDialog", "Port"))
        self.label_4.setText(_translate("ConnectionConfigurationDialog", "User"))
        self.label_5.setText(_translate("ConnectionConfigurationDialog", "Password"))
        self.label_6.setText(_translate("ConnectionConfigurationDialog", "Table"))
        self.pushButtonWriteConf.setText(_translate("ConnectionConfigurationDialog", "Write configuration"))
        self.pushButtonReadConf.setText(_translate("ConnectionConfigurationDialog", "Read configuration"))
        self.pushButtonSave.setText(_translate("ConnectionConfigurationDialog", "Save"))
        self.pushButtonCancel.setText(_translate("ConnectionConfigurationDialog", "Cancel"))


        
class ConnectionConfiguration:
    flagParametersReady:bool
    def __init__(self, funCallBack):
        self.ui = Ui_ConnectionConfigurationDialog()
        self.dialog = QtWidgets.QDialog()
        self.ui.setupUi(self.dialog)
        self.ui.pushButtonReadConf.clicked.connect(self.readConfiguration)
        self.ui.pushButtonWriteConf.clicked.connect(self.writeConfiguration)
        self.ui.pushButtonCancel.clicked.connect(self.cancel)
        self.ui.pushButtonSave.clicked.connect(self.save)
        #self.ui.pushButtonCheck.clicked.connect(self.checkConnection)
        
    def readConfiguration(self):
        fname = QFileDialog.getOpenFileName(self.dialog, 'Open file', os.path.dirname(os.path.realpath(__file__)), "Json files (*.json)")[0]
        try:
            with open(fname, "r") as file:
                data = json.load(file)
            
            self.ui.lineEditHost.setText(data['Settings']['SQL']['Host'])
            self.ui.lineEditDB.setText(data['Settings']['SQL']['Database'])
            self.ui.spinBoxPort.setValue(int(data['Settings']['SQL']['Port']))
            self.ui.lineEditUser.setText(data['Settings']['SQL']['Username'])
            self.ui.lineEditPassword.setText(data['Settings']['SQL']['Password'])
            self.ui.lineEditTable.setText(data['Settings']['SQL']['Table'])
        except Exception as e:
            print("Error while write configuration:", e)
    def writeConfiguration(self):
        try:
            fname = QFileDialog.getSaveFileName(self.dialog, 'Save file', os.path.dirname(os.path.realpath(__file__)), "Json files (*.json)")[0]
            toJson = {'Host':self.ui.lineEditHost.text(), 'Database':self.ui.lineEditDB.text(), 'Port':str(self.ui.spinBoxPort.value()), 'User':self.ui.lineEditUser.text(), 'Password':self.ui.lineEditPassword.text(), 'Table':self.ui.lineEditTable.text()}
            with open(fname, "w") as file:
                json.dump(toJson, file)
        except Exception as e:
            print("Error while write configuration:", e)
    def checkConnection(self):
        self.ui.parameters = DatabaseMYSQL.ParameterConnection(
            user = self.ui.lineEditUser.text(),
            password = self.ui.lineEditPassword.text(),
            host = self.ui.lineEditHost.text(),
            database = self.ui.lineEditDB.text(),
            table = self.ui.lineEditTable.text(),
            port = self.ui.spinBoxPort.value())
        return DatabaseMYSQL.parametersIsValid(self.ui.parameters)
    
    def save(self):
        try:
            self.checkConnection()
            self.flagParametersReady = True
            self.dialog.close()
        except:
            msgBox = QMessageBox()
            msgBox.setText("Connection is unvalid")
            msgBox.setWindowTitle("Status connection")
            msgBox.exec()
            self.flagParametersReady = False
    
    def cancel(self):
        self.flagParametersReady = False
        self.dialog.close()
        
    def show(self):
        self.dialog.exec()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    connectionConfiguration = ConnectionConfiguration()
    connectionConfiguration.show()
    sys.exit(app.exec())
    
    


