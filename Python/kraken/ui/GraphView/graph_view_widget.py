import json, difflib
import os.path

from PySide import QtGui, QtCore

from kraken.ui.GraphView.contextual_node_list import ContextualNodeList, ContextualNewNodeWidget
from kraken.ui.GraphView.graph_view import GraphView
from kraken.ui.undoredo.undo_redo_manager import UndoRedoManager

from kraken.core.objects.rig import Rig
from kraken import plugins


def GetHomePath():
    homeDir = os.path.expanduser("~")
    return homeDir


class GraphViewWidget(QtGui.QWidget):

    rigNameChanged = QtCore.Signal()

    def __init__(self, parent=None):

        # constructors of base classes
        super(GraphViewWidget, self).__init__(parent)
        self.setObjectName('graphViewWidget')
        self.setAttribute(QtCore.Qt.WA_WindowPropagation, True)

        self.graphView = GraphView(parent=self)
        self.__contextualNodeList = None

        #########################
        ## Setup hotkeys for the following actions.
        deleteShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete), self)
        deleteShortcut.activated.connect(self.graphView.deleteSelectedNodes)

        frameShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F), self)
        frameShortcut.activated.connect(self.graphView.frameSelectedNodes)

        frameShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_A), self)
        frameShortcut.activated.connect(self.graphView.frameAllNodes)

        undoShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Z), self)
        undoShortcut.activated.connect(self.undo)

        redoShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Y), self)
        redoShortcut.activated.connect(self.redo)

        openContextualNodeListShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_QuoteLeft), self)
        openContextualNodeListShortcut.activated.connect(self.openContextualNodeList)

        # Setup Layout
        layout = QtGui.QVBoxLayout(self)
        # layout.addWidget(toolBar)
        layout.addWidget(self.graphView)

        self.setLayout(layout)

        self.newRigPreset()

    def getContextualNodeList(self):
        return self.__contextualNodeList

    def editRigName(self):
        dialog = QtGui.QInputDialog(self)
        dialog.setObjectName('RigNameDialog')
        text, ok = dialog.getText(self, 'Edit Rig Name', 'New Rig Name', text=self.guideRig.getName())

        if ok is True:
            self.setRigName(text)


    def setRigName(self, text):
        self.guideRig.setName(text)
        self.rigNameChanged.emit()


    def newRigPreset(self):
        # TODO: clean the rig from the scene if it has been built.
        self.guideRig = Rig()
        self.graphView.displayGraph(self.guideRig)
        self.setRigName('MyRig')


    def saveRigPreset(self):
        lastSceneFilePath = os.path.join(GetHomePath(), self.guideRig.getName() )
        (filePath, filter) = QtGui.QFileDialog.getSaveFileName(self, 'Save Rig Preset', lastSceneFilePath, 'Kraken Rig (*.krg)')
        if len(filePath) > 0:
            self.synchGuideRig()
            self.guideRig.writeRigDefinitionFile(filePath)

    def loadRigPreset(self):
        lastSceneFilePath = GetHomePath()
        (filePath, filter) = QtGui.QFileDialog.getOpenFileName(self, 'Load Rig Preset', lastSceneFilePath, 'Kraken Rig (*.krg)')
        if len(filePath) > 0:
            self.guideRig = Rig()
            self.guideRig.loadRigDefinitionFile(filePath)
            self.graphView.displayGraph( self.guideRig )
            # self.nameWidget.setText( self.guideRig.getName() )

    def buildGuideRig(self):

        self.window().statusBar().showMessage('Building Guide')

        builder = plugins.getBuilder()

        if self.guideRig.getName().endswith('_guide') is False:
            self.guideRig.setName(self.guideRig.getName() + '_guide')

        builder.build(self.guideRig)

        self.window().statusBar().showMessage('Ready')

    def synchGuideRig(self):
        synchronizer = plugins.getSynchronizer()
        synchronizer.setTarget(self.guideRig)
        synchronizer.sync()

    def buildRig(self):

        self.window().statusBar().showMessage('Building Rig')

        self.synchGuideRig()

        rigBuildData = self.guideRig.getRigBuildData()
        rig = Rig()
        rig.loadRigDefinition(rigBuildData)

        rig.setName(rig.getName().replace('_guide', ''))

        builder = plugins.getBuilder()
        builder.build(rig)

        self.window().statusBar().showMessage('Ready')

    # =========
    # Shortcuts
    # =========
    def copy(self):
        graph = self.graphView.getGraph()
        pos = graph.getSelectedNodesPos()
        self.graphView.__class__._clipboardData = graph.copySettings(pos)

    def paste(self):
        graph = self.graphView.getGraph()
        clipboardData = self.graphView.__class__._clipboardData

        pos = clipboardData['copyPos'] + QtCore.QPoint(20, 20)
        graph.pasteSettings(clipboardData, pos, mirrored=False, createConnectionsToExistingNodes=True)

    def pasteUnconnected(self):
        graph = self.graphView.getGraph()
        clipboardData = self.graphView.__class__._clipboardData

        pos = clipboardData['copyPos'] + QtCore.QPoint(20, 20)
        graph.pasteSettings(clipboardData, pos, mirrored=False, createConnectionsToExistingNodes=False)

    def pasteMirrored(self):
        graph = self.graphView.getGraph()
        clipboardData = self.graphView.__class__._clipboardData

        pos = clipboardData['copyPos'] + QtCore.QPoint(20, 20)
        graph.pasteSettings(clipboardData, pos, mirrored=True, createConnectionsToExistingNodes=False)

    def pasteMirroredConnected(self):
        graph = self.graphView.getGraph()
        clipboardData = self.graphView.__class__._clipboardData

        pos = clipboardData['copyPos'] + QtCore.QPoint(20, 20)
        graph.pasteSettings(clipboardData, pos, mirrored=True, createConnectionsToExistingNodes=True)

    def undo(self):
        UndoRedoManager.getInstance().logDebug()
        UndoRedoManager.getInstance().undo()

    def redo(self):
        UndoRedoManager.getInstance().logDebug()
        UndoRedoManager.getInstance().redo()

    def openContextualNodeList(self):
        pos = self.mapFromGlobal(QtGui.QCursor.pos());
        if not self.__contextualNodeList:
            self.__contextualNodeList = ContextualNodeList(self)
        else:
            # Ensures that the node list is reset to list all components
            self.__contextualNodeList.showClosestNames()

        scenepos = self.graphView.mapToScene(pos)
        self.__contextualNodeList.showAtPos(pos, scenepos, self.graphView)

