from ticsummary import ConnectionConfigurationDialog
from ticsummary.CountDetectorsWidget import CountScintillators
from ticsummary.OpenSqlData import OpenSQLData
from ticsummary.ProfilePlotWidget import ProfilePlot
from ticsummary.ViewGraphicsDialog import ViewGraphics
from ticsummary.WaveDetectorsWidget import WaveScintillators
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMenu, QDockWidget, QSplitter


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBoxType = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.comboBoxType.setFont(font)
        self.comboBoxType.setObjectName("comboBoxType")
        self.horizontalLayout.addWidget(self.comboBoxType)
        self.pushButtonPrev = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferDefault)
        self.pushButtonPrev.setFont(font)
        self.pushButtonPrev.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.pushButtonPrev.setAutoFillBackground(False)
        self.pushButtonPrev.setFlat(False)
        self.pushButtonPrev.setObjectName("pushButtonPrev")
        self.horizontalLayout.addWidget(self.pushButtonPrev)
        self.pushButtonNext = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButtonNext.setFont(font)
        self.pushButtonNext.setObjectName("pushButtonNext")
        self.horizontalLayout.addWidget(self.pushButtonNext)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayoutGraphics = QtWidgets.QHBoxLayout()
        self.horizontalLayoutGraphics.setObjectName("horizontalLayoutGraphics")
        self.verticalLayout.addLayout(self.horizontalLayoutGraphics)
        self.progressBarTask = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBarTask.setProperty("value", 24)
        self.progressBarTask.setObjectName("progressBarTask")
        self.verticalLayout.addWidget(self.progressBarTask)
        self.horizontalLayout_Information = QtWidgets.QHBoxLayout()
        self.horizontalLayout_Information.setObjectName("horizontalLayout_Information")
        self.verticalLayout.addLayout(self.horizontalLayout_Information)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 34))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.menubar.setFont(font)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.menuFile.setFont(font)
        self.menuFile.setObjectName("menuFile")
        self.menuOpen = QtWidgets.QMenu(self.menuFile)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.menuOpen.setFont(font)
        self.menuOpen.setObjectName("menuOpen")
        self.menuExport = QtWidgets.QMenu(self.menuFile)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.menuExport.setFont(font)
        self.menuExport.setObjectName("menuExport")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.menuEdit.setFont(font)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionFrom_sql_database = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.actionFrom_sql_database.setFont(font)
        self.actionFrom_sql_database.setObjectName("actionFrom_sql_database")
        self.actionmeasured_data_to_csv = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.actionmeasured_data_to_csv.setFont(font)
        self.actionmeasured_data_to_csv.setObjectName("actionmeasured_data_to_csv")
        self.actionConnectionSqlDatabase = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.actionConnectionSqlDatabase.setFont(font)
        self.actionConnectionSqlDatabase.setObjectName("actionConnectionSqlDatabase")
        self.actionPlots = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.actionPlots.setFont(font)
        self.actionPlots.setObjectName("actionPlots")
        self.menuOpen.addAction(self.actionFrom_sql_database)
        self.menuExport.addAction(self.actionmeasured_data_to_csv)
        self.menuFile.addAction(self.menuOpen.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuExport.menuAction())
        self.menuEdit.addAction(self.actionConnectionSqlDatabase)
        self.menuView.addAction(self.actionPlots)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButtonPrev.setText(_translate("MainWindow", "Prev"))
        self.pushButtonNext.setText(_translate("MainWindow", "Next"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuOpen.setTitle(_translate("MainWindow", "Open.."))
        self.menuExport.setTitle(_translate("MainWindow", "Export.."))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.actionFrom_sql_database.setText(_translate("MainWindow", "From sql database"))
        self.actionmeasured_data_to_csv.setText(_translate("MainWindow", "measured data to csv"))
        self.actionConnectionSqlDatabase.setText(_translate("MainWindow", "Connection to sql database"))
        self.actionPlots.setText(_translate("MainWindow", "Plots"))


class MainWindow():
    def __init__(self):
        self.ui = Ui_MainWindow()
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui.setupUi(self.MainWindow)
        self.ui.actionConnectionSqlDatabase.triggered.connect(self.openConnectionConfiguration)
        self.ui.actionPlots.triggered.connect(self.openViewGraphics)
        self.ui.actionFrom_sql_database.triggered.connect(self.openSQLData)
        
        
        self.profilePlotMCPX1 = ProfilePlot("MCP X 1")
        self.addWidgetToCentralLayout(self.profilePlotMCPX1.getWidget())
        self.profilePlotMCPX2 = ProfilePlot("MCP X 2")
        self.addWidgetToCentralLayout(self.profilePlotMCPX2.getWidget())
        self.profilePlotMCPY1 = ProfilePlot("MCP Y 1")
        self.addWidgetToCentralLayout(self.profilePlotMCPY1.getWidget())
        self.profilePlotMCPY2 = ProfilePlot("MCP Y 2")
        self.addWidgetToCentralLayout(self.profilePlotMCPY2.getWidget())
        self.waveDetectors = WaveScintillators("Galo Beam")
        self.addWidgetToCentralLayout(self.waveDetectors.getWidget())
        self.countDetectors = CountScintillators()
        self.addWidgetToCentralLayout(self.countDetectors.getWidget())
    
    def openConnectionConfiguration(self):
        connectionConfigurationDialog = ConnectionConfigurationDialog.ConnectionConfiguration(lambda self, answer, result: self.setNewConnectionconfiguration(result) if(answer) else None)
        connectionConfigurationDialog.show()
    def setNewConnectionConfiguration(self, configuration):
        self.sqlConfiguration = configuration 
    def openViewGraphics(self):
        self.viewGraphics = ViewGraphics(self.ui.centralwidget , not self.profilePlotMCPX1.getWidget().isHidden(), not self.profilePlotMCPX2.getWidget().isHidden(), not self.profilePlotMCPY1.getWidget().isHidden(),not self.profilePlotMCPY2.getWidget().isHidden(), not self.waveDetectors.getWidget().isHidden(), not self.countDetectors.getWidget().isHidden())
        self.viewGraphics.getUI().checkBoxMCPX1.stateChanged.connect(lambda state: self.setHideWidget(self.profilePlotMCPX1.getWidget(),not state))
        self.viewGraphics.getUI().checkBoxMCPX2.stateChanged.connect(lambda state: self.setHideWidget(self.profilePlotMCPX2.getWidget(),not state))
        self.viewGraphics.getUI().checkBoxMCPY1.stateChanged.connect(lambda state: self.setHideWidget(self.profilePlotMCPY1.getWidget(),not state))
        self.viewGraphics.getUI().checkBoxMCPY2.stateChanged.connect(lambda state: self.setHideWidget(self.profilePlotMCPY2.getWidget(),not state))
        self.viewGraphics.getUI().checkBoxWaveDetectors.stateChanged.connect(lambda state: self.setHideWidget(self.waveDetectors.getWidget(),not state))
        self.viewGraphics.getUI().checkBoxCountDetectors.stateChanged.connect(lambda state: self.setHideWidget(self.countDetectors.getWidget(),not state))
        self.viewGraphics.show()
    def openSQLData(self):
        self.openSQLData = OpenSQLData()
        self.openSQLData.show()
    def addWidgetToCentralLayout(self, widget):
        i = 5
        #self.ui.splitter.addWidget(widget)
    def addDockWidgetToCentralLayout(self, widget):
        window = self.ui.mdiAreaGraphics.addSubWindow(widget)
        window.setWindowTitle("JHi")
        self.ui.mdiAreaGraphics.tileSubWindows()
    def show(self):
        self.MainWindow.show()
    def setHideWidget(self, widget, state):
        widget.setHidden(state)
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec())
    
    
    
