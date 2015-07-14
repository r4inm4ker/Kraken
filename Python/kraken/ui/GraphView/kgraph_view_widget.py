import json, difflib
import os.path

from PySide import QtGui, QtCore

from contextual_node_list import ContextualNodeList, ContextualNewNodeWidget
from graph_view.graph_view_widget import GraphViewWidget
from kraken.ui.undoredo.undo_redo_manager import UndoRedoManager

from graph_commands import AddNodeCommand, RemoveNodeCommand, ConnectionAddedCommand, ConnectionRemovedCommand

from kraken.core.objects.rig import Rig
from kraken import plugins


def GetHomePath():
    homeDir = os.path.expanduser("~")
    return homeDir


class KGraphViewWidget(GraphViewWidget):

    rigNameChanged = QtCore.Signal()

    def __init__(self, parent=None):

        # constructors of base classes
        super(KGraphViewWidget, self).__init__(parent)
        self.__contextualNodeList = None

        #########################
        ## Setup hotkeys for the following actions.

        undoShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Z), self)
        undoShortcut.activated.connect(self.undo)

        redoShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Y), self)
        redoShortcut.activated.connect(self.redo)

        openContextualNodeListShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_QuoteLeft), self)
        openContextualNodeListShortcut.activated.connect(self.openContextualNodeList)

        self.newRigPreset()

        self.graphView.nodeAdded.connect(self.__onNodeAdded)
        self.graphView.nodeRemoved.connect(self.__onNodeRemoved)
        self.graphView.beginConnectionManipulation.connect(self.__onBeginConnectionManipulation)
        self.graphView.endConnectionManipulation.connect(self.__onEndConnectionManipulationSignal)
        self.graphView.connectionAdded.connect(self.__onConnectionAdded)
        self.graphView.connectionRemoved.connect(self.__onConnectionRemoved)

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
        UndoRedoManager.getInstance().undo()
        UndoRedoManager.getInstance().logDebug()

    def redo(self):
        UndoRedoManager.getInstance().redo()
        UndoRedoManager.getInstance().logDebug()

    def openContextualNodeList(self):
        pos = self.mapFromGlobal(QtGui.QCursor.pos());
        if not self.__contextualNodeList:
            self.__contextualNodeList = ContextualNodeList(self)
        else:
            # Ensures that the node list is reset to list all components
            self.__contextualNodeList.showClosestNames()

        scenepos = self.graphView.mapToScene(pos)
        self.__contextualNodeList.showAtPos(pos, scenepos, self.graphView)


    def __onNodeAdded(self, node):
        command = AddNodeCommand(self.graphView, self.guideRig, node)
        UndoRedoManager.getInstance().addCommand(command, invokeRedoOnAdd=False)

    def __onNodeRemoved(self, node):
        print "__onNodeRemoved:" + str(node)
        command = RemoveNodeCommand(self.graphView, self.guideRig, node)
        UndoRedoManager.getInstance().addCommand(command, invokeRedoOnAdd=False)


    def __onBeginConnectionManipulation(self):
        print "__onBeginConnectionManipulation:"
        UndoRedoManager.getInstance().openBracket('Connect Ports')


    def __onEndConnectionManipulationSignal(self):
        print "__onEndConnectionManipulationSignal:"
        UndoRedoManager.getInstance().closeBracket()


    def __onConnectionAdded(self, connection):
        print "__onConnectionAdded:" + str(connection)

        command = ConnectionAddedCommand(self.graphView, self.guideRig, connection)
        UndoRedoManager.getInstance().addCommand(command, invokeRedoOnAdd=False)


    def __onConnectionRemoved(self, connection):
        print "__onConnectionRemoved:" + str(connection)

        command = ConnectionRemovedCommand(self.graphView, self.guideRig, connection)
        UndoRedoManager.getInstance().addCommand(command, invokeRedoOnAdd=False)

