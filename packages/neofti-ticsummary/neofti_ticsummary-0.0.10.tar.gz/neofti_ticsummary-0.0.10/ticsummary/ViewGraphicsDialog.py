from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ViewGraphicsDialog(object):
    def setupUi(self, ViewGraphicsDialog):
        ViewGraphicsDialog.setObjectName("ViewGraphicsDialog")
        ViewGraphicsDialog.resize(158, 200)
        ViewGraphicsDialog.setMinimumSize(QtCore.QSize(140, 200))
        self.verticalLayout = QtWidgets.QVBoxLayout(ViewGraphicsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBoxMCPX1 = QtWidgets.QCheckBox(ViewGraphicsDialog)
        self.checkBoxMCPX1.setObjectName("checkBoxMCPX1")
        self.verticalLayout.addWidget(self.checkBoxMCPX1)
        self.checkBoxMCPX2 = QtWidgets.QCheckBox(ViewGraphicsDialog)
        self.checkBoxMCPX2.setObjectName("checkBoxMCPX2")
        self.verticalLayout.addWidget(self.checkBoxMCPX2)
        self.checkBoxMCPY1 = QtWidgets.QCheckBox(ViewGraphicsDialog)
        self.checkBoxMCPY1.setObjectName("checkBoxMCPY1")
        self.verticalLayout.addWidget(self.checkBoxMCPY1)
        self.checkBoxMCPY2 = QtWidgets.QCheckBox(ViewGraphicsDialog)
        self.checkBoxMCPY2.setObjectName("checkBoxMCPY2")
        self.verticalLayout.addWidget(self.checkBoxMCPY2)
        self.checkBoxCountDetectors = QtWidgets.QCheckBox(ViewGraphicsDialog)
        self.checkBoxCountDetectors.setObjectName("checkBoxCountDetectors")
        self.verticalLayout.addWidget(self.checkBoxCountDetectors)
        self.checkBoxWaveDetectors = QtWidgets.QCheckBox(ViewGraphicsDialog)
        self.checkBoxWaveDetectors.setObjectName("checkBoxWaveDetectors")
        self.verticalLayout.addWidget(self.checkBoxWaveDetectors)
        self.pushButtonClose = QtWidgets.QPushButton(ViewGraphicsDialog)
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.verticalLayout.addWidget(self.pushButtonClose)

        self.retranslateUi(ViewGraphicsDialog)
        QtCore.QMetaObject.connectSlotsByName(ViewGraphicsDialog)

    def retranslateUi(self, ViewGraphicsDialog):
        _translate = QtCore.QCoreApplication.translate
        ViewGraphicsDialog.setWindowTitle(_translate("ViewGraphicsDialog", "Edit plots"))
        self.checkBoxMCPX1.setText(_translate("ViewGraphicsDialog", "MCP X B1"))
        self.checkBoxMCPX2.setText(_translate("ViewGraphicsDialog", "MCP X B2"))
        self.checkBoxMCPY1.setText(_translate("ViewGraphicsDialog", "MCP Y B1"))
        self.checkBoxMCPY2.setText(_translate("ViewGraphicsDialog", "MCP Y B2"))
        self.checkBoxCountDetectors.setText(_translate("ViewGraphicsDialog", "Count Detectors"))
        self.checkBoxWaveDetectors.setText(_translate("ViewGraphicsDialog", "Wave Detectors"))
        self.pushButtonClose.setText(_translate("ViewGraphicsDialog", "Close"))


class ViewGraphics:
    ui: Ui_ViewGraphicsDialog
    def __init__(self, parent, checkBoxMCPX1Enabled, checkBoxMCPX2Enabled, checkBoxMCPY1Enabled, checkBoxMCPY2Enabled, checkBoxCountDetectorsEnabled, checkBoxWaveDetectorsEnabled):
        self.ui = Ui_ViewGraphicsDialog()
        self.dialog = QtWidgets.QDialog(parent)
        self.ui.setupUi(self.dialog)
        self.ui.checkBoxMCPX1.setChecked(checkBoxMCPX1Enabled)
        self.ui.checkBoxMCPX2.setChecked(checkBoxMCPX2Enabled)
        self.ui.checkBoxMCPY1.setChecked(checkBoxMCPY1Enabled)
        self.ui.checkBoxMCPY2.setChecked(checkBoxMCPY2Enabled)
        self.ui.checkBoxCountDetectors.setChecked(checkBoxCountDetectorsEnabled)
        self.ui.checkBoxWaveDetectors.setChecked(checkBoxWaveDetectorsEnabled)
        self.ui.pushButtonClose.clicked.connect(self.actionClose)
        
    def show(self):
        self.dialog.show()
    def actionClose(self):
        self.dialog.close()
    def getUI(self):
        return self.ui

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    viewGraphics = ViewGraphics(False,False,True,True,True,True)
    viewGraphics.show()
    sys.exit(app.exec())

