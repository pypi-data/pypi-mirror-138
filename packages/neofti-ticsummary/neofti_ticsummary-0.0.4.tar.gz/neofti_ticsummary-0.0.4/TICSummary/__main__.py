from PyQt6 import QtCore, QtGui, QtWidgets   
import MainWindow, ConnectionConfigurationDialog, DatabaseMYSQL, Plot

class EntryPoint:
    sqlParameters:DatabaseMYSQL.ParameterConnection
    profilePlot1: Plot
    
    def run(self):
        import sys
        app = QtWidgets.QApplication(sys.argv)
        self.mainWindow = MainWindow.MainWindow()
        
        self.mainWindow.show()
        sys.exit(app.exec())
    
    
if __name__ == '__main__':
    entryPoint = EntryPoint()
    entryPoint.run()