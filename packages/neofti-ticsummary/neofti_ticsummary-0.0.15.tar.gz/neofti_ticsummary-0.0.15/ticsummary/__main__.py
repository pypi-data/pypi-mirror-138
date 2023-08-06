from PyQt6 import QtCore, QtGui, QtWidgets   
from ticsummary import MainWindow, ConnectionConfigurationDialog, DatabaseMYSQL, Plot

class EntryPoint:
    sqlParameters:DatabaseMYSQL.ParameterConnection
    profilePlot1: Plot
    
    def run(self):
        import sys
        app = QtWidgets.QApplication(sys.argv)
        self.mainWindow = MainWindow.MainWindow()
        
        self.mainWindow.show()
        sys.exit(app.exec())

 
    
def startup():
    entryPoint = EntryPoint()
    entryPoint.run()