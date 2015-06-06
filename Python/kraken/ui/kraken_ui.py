
#
# Copyright 2010-2015
#

import sys
from PySide import QtGui, QtCore
from component_library import ComponentLibrary
from GraphView.graph_view_widget import GraphViewWidget

from kraken.core.kraken_system import KrakenSystem

class KrakenUI(QtGui.QWidget):
    """A debugger widget hosting an inspector as well as a graph view"""

    def __init__(self, parent=None):

        # constructors of base classes
        super(KrakenUI, self).__init__(parent)

        self.setWindowTitle("Kraken Editor")
        self.setAcceptDrops(True)

        self.nodeLibrary = ComponentLibrary(parent=self)
        self.graphViewWidget = GraphViewWidget(parent=self)

        horizontalSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal, parent=self)
        horizontalSplitter.addWidget(self.nodeLibrary)
        horizontalSplitter.addWidget(self.graphViewWidget)

        horizontalSplitter.setStretchFactor(0, 0)
        horizontalSplitter.setStretchFactor(1, 1)

        grid = QtGui.QVBoxLayout(self)
        grid.addWidget(horizontalSplitter)

    def closeEvent(self, event):
        self.graphViewWidget.closeEvent(event)

    def showEvent(self, event):
        krakenSystem = KrakenSystem.getInstance()
        krakenSystem.loadCoreClient()
        krakenSystem.loadExtension('Kraken')


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    widget = KrakenUI()
    widget.show()
    sys.exit(app.exec_())
