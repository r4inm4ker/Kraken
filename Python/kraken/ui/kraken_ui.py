
import os
import sys

from PySide import QtGui, QtCore

from kraken.core.kraken_system import KrakenSystem
from kraken.log import getLogger
from kraken.ui.component_library import ComponentLibrary
from kraken.ui.GraphView.kgraph_view_widget import KGraphViewWidget
import kraken.ui.images_rc

logger = getLogger('kraken')


class KrakenUI(QtGui.QWidget):
    """A debugger widget hosting an inspector as well as a graph view"""

    def __init__(self, parent=None):

        # constructors of base classes
        super(KrakenUI, self).__init__(parent)
        self.setObjectName('mainUI')
        self.setWindowIcon(QtGui.QIcon(':/images/Kraken_Icon.png'))

        self.setWindowTitle("Kraken Editor")
        self.setAcceptDrops(True)

        self.graphViewWidget = KGraphViewWidget(parent=self)
        self.nodeLibrary = ComponentLibrary(parent=self)

        self.horizontalSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal, parent=self)
        self.horizontalSplitter.addWidget(self.nodeLibrary)
        self.horizontalSplitter.addWidget(self.graphViewWidget)

        self.horizontalSplitter.setStretchFactor(0, 0)
        self.horizontalSplitter.setStretchFactor(1, 1)
        self.horizontalSplitter.setSizes([0, 100])
        self.horizontalSplitter.splitterMoved.connect(self.splitterMoved)
        self.nodeLibraryExpandedSize = 175

        grid = QtGui.QVBoxLayout(self)
        grid.addWidget(self.horizontalSplitter)


    def showEvent(self, event):

        krakenSystem = KrakenSystem.getInstance()
        krakenSystem.loadCoreClient()
        krakenSystem.loadExtension('Kraken')

        # Need to wait until window is shown before we update the statusBar with messages
        if hasattr(self, "error_loading_startup"):

            if self.error_loading_startup:
                logger.error('Error Loading Modules')
            else:
                logger.info('Success Loading Modules')

            delattr(self, "error_loading_startup")

    def resizeSplitter(self):
        splitter = self.horizontalSplitter
        sizes = splitter.sizes()

        if sizes[0] == 0:
            splitter.setSizes([self.nodeLibraryExpandedSize, sizes[1]])
        else:
            splitter.setSizes([0, sizes[1]])

    def splitterMoved(self, pos, index):
        self.nodeLibraryExpandedSize = pos

    def writeSettings(self, settings):
        settings.beginGroup("KrakenUI")
        settings.setValue('horizontalSplitterSizes', self.nodeLibraryExpandedSize)
        settings.setValue('componentLibCollapsed', self.horizontalSplitter.sizes()[0] == 0)
        settings.endGroup()

    def readSettings(self, settings):
        settings.beginGroup("KrakenUI")
        if settings.contains('horizontalSplitterSizes'):
            self.nodeLibraryExpandedSize = settings.value('horizontalSplitterSizes', 175)
        if settings.contains('componentLibCollapsed'):
            if settings.value('componentLibCollapsed') == 'false':
                splitter = self.horizontalSplitter
                sizes = splitter.sizes()

                self.horizontalSplitter.setSizes([self.nodeLibraryExpandedSize, sizes[1]])

        settings.endGroup()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    widget = KrakenUI()
    widget.show()

    sys.exit(app.exec_())
