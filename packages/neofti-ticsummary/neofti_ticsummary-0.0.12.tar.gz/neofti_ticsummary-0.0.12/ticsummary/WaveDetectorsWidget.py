from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QObject
from ticsummary import Plot, DataTIC


class WaveScintillators(Plot.Ui_Plot):
    def __init__(self, title):
        super().__init__()
        self.form = QtWidgets.QWidget()
        super().setupUi(self.form)
        for item in DataTIC.MeasureWaveDetectorsEnum:
            self.addItemcomboBoxTypePlot(item.title)
        super().setMainTitle(title)
    def getWidget(self):
        return self.form