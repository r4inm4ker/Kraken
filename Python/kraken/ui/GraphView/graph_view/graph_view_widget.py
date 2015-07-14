
#
# Copyright 2010-2015
#

from PySide import QtGui, QtCore

from graph_view import GraphView

class GraphViewWidget(QtGui.QWidget):

    rigNameChanged = QtCore.Signal()

    def __init__(self, parent=None):

        # constructors of base classes
        super(GraphViewWidget, self).__init__(parent)
        self.setObjectName('graphViewWidget')
        self.setAttribute(QtCore.Qt.WA_WindowPropagation, True)


    def setGraphView(self, graphView):

        self.graphView = graphView

        # Setup Layout
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.graphView)
        self.setLayout(layout)

        #########################
        ## Setup hotkeys for the following actions.
        deleteShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete), self)
        deleteShortcut.activated.connect(self.graphView.deleteSelectedNodes)

        frameShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F), self)
        frameShortcut.activated.connect(self.graphView.frameSelectedNodes)

        frameShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_A), self)
        frameShortcut.activated.connect(self.graphView.frameAllNodes)


    def getGraphView(self):
        return self.graphView