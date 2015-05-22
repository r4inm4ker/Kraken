
#
# Copyright 2010-2015
#

import sys
from PySide import QtGui, QtCore
from node_library import NodeLibrary
from GraphView.graph_view import GraphViewWidget

from kraken.core.objects.rig import Rig
from kraken.examples.bob_guide_data import bob_guide_data


class GraphEditor(QtGui.QWidget):
    """A debugger widget hosting an inspector as well as a graph view"""

    def __init__(self, parent=None):

        # constructors of base classes
        super(GraphEditor, self).__init__(parent)

        #self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea | QtCore.Qt.BottomDockWidgetArea | QtCore.Qt.TopDockWidgetArea)
        self.setAcceptDrops(True)

        self.rig = Rig()
        self.rig.loadRigDefinition(bob_guide_data)

        self.nodeLibrary = NodeLibrary(self)
        self.graphViewWidget = GraphViewWidget(self.rig, self)

        horizontalSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal,self)
        horizontalSplitter.addWidget(self.nodeLibrary)
        horizontalSplitter.addWidget(self.graphViewWidget)

        horizontalSplitter.setStretchFactor(0, 0)
        horizontalSplitter.setStretchFactor(1, 1)


        grid = QtGui.QVBoxLayout(self)
        grid.addWidget(horizontalSplitter)

        # self.setWindowTitle("Kraken Node Editor")
        # self.setWidget(horizontalSplitter)

    def closeEvent(self, event):
        pass
        # self.__graphViewWidget.closeEvent(event)
        # return super(GraphEditor, self).closeEvent(event)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    widget = GraphEditor()
    widget.show()
    sys.exit(app.exec_())

