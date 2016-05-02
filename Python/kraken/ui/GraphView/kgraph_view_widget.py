import difflib
import json
import logging
import os
import re
import traceback

from PySide import QtGui, QtCore

from kbackdrop import KBackdrop
from contextual_node_list import ContextualNodeList
from pyflowgraph.graph_view_widget import GraphViewWidget
from kgraph_view import KGraphView
from kraken.ui.undoredo.undo_redo_manager import UndoRedoManager
import graph_commands

from kraken.log import getLogger
from kraken.core.objects.rig import Rig
from kraken import plugins

logger = getLogger('kraken')


def GetKrakenPath():
    if 'KRAKEN_PATH' in os.environ:
        return os.environ['KRAKEN_PATH']
    return os.path.expanduser("~")


class KGraphViewWidget(GraphViewWidget):

    rigNameChanged = QtCore.Signal()
    rigLoaded = QtCore.Signal(object)

    def __init__(self, parent=None):

        # constructors of base classes
        super(KGraphViewWidget, self).__init__(parent)

        self._builder = None
        self._guideBuilder = None

        graphView = KGraphView(parent=self)
        graphView.nodeAdded.connect(self.__onNodeAdded)
        graphView.nodeRemoved.connect(self.__onNodeRemoved)
        graphView.beginConnectionManipulation.connect(self.__onBeginConnectionManipulation)
        graphView.endConnectionManipulation.connect(self.__onEndConnectionManipulationSignal)
        graphView.connectionAdded.connect(self.__onConnectionAdded)
        graphView.connectionRemoved.connect(self.__onConnectionRemoved)

        graphView.selectionChanged.connect(self.__onSelectionChanged)
        graphView.endSelectionMoved.connect(self.__onSelectionMoved)

        graphView.beginDeleteSelection.connect(self.__onBeginDeleteSelection)
        graphView.endDeleteSelection.connect(self.__onEndDeleteSelection)

        self.setGraphView(graphView)

        #########################
        ## Setup hotkeys for the following actions.

        undoShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Z), self)
        undoShortcut.activated.connect(self.undo)

        redoShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Y), self)
        redoShortcut.activated.connect(self.redo)

        openContextualNodeListShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Tab), self)
        openContextualNodeListShortcut.activated.connect(self.openContextualNodeList)

        self.newRigPreset()


    # ============
    # Rig Methods
    # ============
    def editRigName(self):
        dialog = QtGui.QInputDialog(self)
        dialog.setObjectName('RigNameDialog')
        text, ok = dialog.getText(self, 'Edit Rig Name', 'New Rig Name', text=self.guideRig.getName())

        if ok is True:
            self.setGuideRigName(text)

    def setGuideRigName(self, text):


        if text.endswith('_guide') is True:
            text = text.replace('_guide', '')

        self.guideRig.setName(text)
        self.rigNameChanged.emit()

    def newRigPreset(self):
        logger.debug("New Rig")

        try:

            self.guideRig = Rig()
            self.getGraphView().displayGraph(self.guideRig)
            self.setGuideRigName('MyRig')

            self.openedFile = None

            self.window().setWindowTitle('Kraken Editor')

        except Exception as e:
            logger.exception("Error Creating New Rig")

    def saveRig(self, saveAs=False):
        """Saves the current rig to disc.

        Args:
            saveAs (Boolean): Determines if this was a save as call or just a normal save.

        Returns:
            String: Path to the saved file.

        """

        try:
            self.window().setCursor(QtCore.Qt.WaitCursor)

            filePath = self.openedFile

            if saveAs is True or not filePath or not os.path.isdir(os.path.dirname(filePath)):

                settings = self.window().getSettings()
                settings.beginGroup('Files')
                lastFilePath = settings.value("lastFilePath", os.path.join(GetKrakenPath(), self.guideRig.getName()))
                settings.endGroup()

                filePathDir = os.path.dirname(lastFilePath)

                if not os.path.isdir(filePathDir):
                    filePathDir = GetKrakenPath()

                fileDialog = QtGui.QFileDialog(self)
                fileDialog.setOption(QtGui.QFileDialog.DontUseNativeDialog, on=True)
                fileDialog.setWindowTitle('Save Rig Preset As')
                fileDialog.setDirectory(os.path.abspath(filePathDir))
                fileDialog.setAcceptMode(QtGui.QFileDialog.AcceptSave)
                fileDialog.setNameFilter('Kraken Rig (*.krg)')
                fileDialog.setDefaultSuffix('krg')

                if fileDialog.exec_() == QtGui.QFileDialog.Accepted:
                    filePath = fileDialog.selectedFiles()[0]
                else:
                    return False

            self.synchGuideRig()

            # Backdrop Meta Data
            graphView = self.getGraphView()
            backdropNodes = graphView.getNodesOfType('KBackdrop')
            backdropData = [x.getData() for x in backdropNodes]

            # Add Meta Data to rig
            self.guideRig.setMetaData('backdrops', backdropData)

            # Write rig file
            try:
                self.guideRig.writeRigDefinitionFile(filePath)
                settings = self.window().getSettings()
                settings.beginGroup('Files')
                settings.setValue("lastFilePath", filePath)
                settings.endGroup()
                self.openedFile = filePath

                logger.info('Saved Rig file: ' + filePath)

            except Exception as e:
                logger.exception('Error Saving Rig File')
                return False

            return filePath

        finally:
            self.window().setCursor(QtCore.Qt.ArrowCursor)

    def saveAsRigPreset(self):
        """Opens a dialogue window to save the current rig as a different file."""

        filePath = self.saveRig(saveAs=True)
        if filePath is not False:
            self.window().setWindowTitle('Kraken Editor - ' + filePath + '[*]')

        self.rigLoaded.emit(self.openedFile)

    def saveRigPreset(self):

        if self.openedFile is None or not os.path.exists(self.openedFile):
            self.saveAsRigPreset()

        else:
            self.saveRig(saveAs=False)
            self.rigLoaded.emit(self.openedFile)

    def openRigPreset(self):

        try:
            self.window().setCursor(QtCore.Qt.WaitCursor)

            settings = self.window().getSettings()
            settings.beginGroup('Files')
            lastFilePath = settings.value("lastFilePath", os.path.join(GetKrakenPath(), self.guideRig.getName()))
            settings.endGroup()

            if not lastFilePath:
                lastFilePath = GetKrakenPath()

            fileDialog = QtGui.QFileDialog(self)
            fileDialog.setOption(QtGui.QFileDialog.DontUseNativeDialog, on=True)
            fileDialog.setWindowTitle('Open Rig Preset')
            fileDialog.setDirectory(os.path.dirname(os.path.abspath(lastFilePath)))
            fileDialog.setAcceptMode(QtGui.QFileDialog.AcceptOpen)
            fileDialog.setNameFilter('Kraken Rig (*.krg)')

            if fileDialog.exec_() == QtGui.QFileDialog.Accepted:
                filePath = fileDialog.selectedFiles()[0]
                self.loadRigPreset(filePath)

        finally:
            self.window().setCursor(QtCore.Qt.ArrowCursor)

    def loadRigPreset(self, filePath):
        self.guideRig = Rig()
        self.guideRig.loadRigDefinitionFile(filePath)
        self.setGuideRigName(self.guideRig.getName())  # Remove "_guide" from end of name
        self.graphView.displayGraph(self.guideRig)

        settings = self.window().getSettings()
        settings.beginGroup('Files')
        settings.setValue("lastFilePath", filePath)
        settings.endGroup()

        self.openedFile = filePath
        self.window().setWindowTitle('Kraken Editor - ' + filePath + '[*]')
        logger.info('Loaded Rig file: ' + filePath)

        self.rigLoaded.emit(filePath)

    def buildGuideRig(self):

        try:
            logger.info('Building Guide')
            self.window().setCursor(QtCore.Qt.WaitCursor)

            # self.window().statusBar().showMessage('Building Guide')

            initConfigIndex = self.window().krakenMenu.configsWidget.currentIndex()

            builder = plugins.getBuilder()

            # Append "_guide" to rig name when building guide
            if self.guideRig.getName().endswith('_guide') is False:
                self.guideRig.setName(self.guideRig.getName() + '_guide')

            if self.window().preferences.getPreferenceValue('delete_existing_rigs'):
                if self._guideBuilder:
                    self._guideBuilder.deleteBuildElements()

            self._guideBuilder = plugins.getBuilder()
            self._guideBuilder.buildRig(self.guideRig)

            logger.info('Guide Rig Build Success')

            self.window().krakenMenu.setCurrentConfig(initConfigIndex)

        except Exception as e:
            logger.exception('Error Building')

        finally:
            self.window().setCursor(QtCore.Qt.ArrowCursor)

    def synchGuideRig(self):
        synchronizer = plugins.getSynchronizer()

        # Guide is always  built with "_guide" need this so synchronizer not confused with real Rig nodes
        if self.guideRig.getName().endswith('_guide') is False:
            self.guideRig.setName(self.guideRig.getName() + '_guide')

        synchronizer.setTarget(self.guideRig)
        synchronizer.sync()

    def buildRig(self):

        try:
            self.window().setCursor(QtCore.Qt.WaitCursor)

            self.window().statusBar.showMessage('Building Rig')

            initConfigIndex = self.window().krakenMenu.configsWidget.currentIndex()

            self.synchGuideRig()

            rigBuildData = self.guideRig.getRigBuildData()
            rig = Rig()
            rig.loadRigDefinition(rigBuildData)

            rig.setName(rig.getName().replace('_guide', ''))

            if self.window().preferences.getPreferenceValue('delete_existing_rigs'):
                if self._builder:
                    self._builder.deleteBuildElements()

            self._builder = plugins.getBuilder()
            self._builder.buildRig(rig)

            logger.info('Rig Build Success')

            self.window().krakenMenu.setCurrentConfig(initConfigIndex)

        except Exception as e:
            logger.exception('Error Building')

        finally:
            self.window().setCursor(QtCore.Qt.ArrowCursor)

    # ==========
    # Shortcuts
    # ==========
    def copy(self):
        graphView = self.getGraphView()
        pos = graphView.getSelectedNodesCentroid()
        graphView.copySettings(pos)

    def paste(self):
        graphView = self.getGraphView()
        clipboardData = self.graphView.getClipboardData()

        pos = clipboardData['copyPos'] + QtCore.QPoint(20, 20)
        graphView.pasteSettings(pos, mirrored=False, createConnectionsToExistingNodes=True)

    def pasteUnconnected(self):
        graphView = self.getGraphView()
        clipboardData = self.graphView.getClipboardData()

        pos = clipboardData['copyPos'] + QtCore.QPoint(20, 20)
        graphView.pasteSettings(pos, mirrored=False, createConnectionsToExistingNodes=False)

    def pasteMirrored(self):
        graphView = self.getGraphView()
        clipboardData = self.graphView.getClipboardData()

        pos = clipboardData['copyPos'] + QtCore.QPoint(20, 20)
        graphView.pasteSettings(pos, mirrored=True, createConnectionsToExistingNodes=False)

    def pasteMirroredConnected(self):
        graphView = self.getGraphView()
        clipboardData = self.graphView.getClipboardData()

        pos = clipboardData['copyPos'] + QtCore.QPoint(20, 20)
        graphView.pasteSettings(pos, mirrored=True, createConnectionsToExistingNodes=True)

    def undo(self):
        UndoRedoManager.getInstance().undo()

    def redo(self):
        UndoRedoManager.getInstance().redo()

    def openContextualNodeList(self):
        pos = self.mapFromGlobal(QtGui.QCursor.pos())

        contextualNodeList = ContextualNodeList(self)

        scenepos = self.graphView.mapToScene(pos)
        contextualNodeList.showAtPos(pos, scenepos, self.graphView)

    # ==============
    # Other Methods
    # ==============
    def addBackdrop(self, name='Backdrop'):
        """Adds a backdrop node to the graph.

        Args:
            name (str): Name of the backdrop node.

        Returns:
            Node: Backdrop node that was created.

        """

        graphView = self.getGraphView()

        initName = name
        suffix = 1
        collision = True
        while collision:

            collision = graphView.hasNode(name)
            if not collision:
                break

            result = re.split(r"(\d+)$", initName, 1)
            if len(result) > 1:
                initName = result[0]
                suffix = int(result[1])

            name = initName + str(suffix).zfill(2)
            suffix += 1

        backdropNode = KBackdrop(graphView, name)
        graphView.addNode(backdropNode)

        graphView.selectNode(backdropNode, clearSelection=True)

        return backdropNode

    # ===============
    # Signal Handlers
    # ===============
    def __onNodeAdded(self, node):
        if not UndoRedoManager.getInstance().isUndoingOrRedoing():
            command = graph_commands.AddNodeCommand(self.graphView, self.guideRig, node)
            UndoRedoManager.getInstance().addCommand(command)

    def __onNodeRemoved(self, node):

        if type(node).__name__ != 'KBackdrop':
            node.getComponent().detach()

        if not UndoRedoManager.getInstance().isUndoingOrRedoing():
            command = graph_commands.RemoveNodeCommand(self.graphView, self.guideRig, node)
            UndoRedoManager.getInstance().addCommand(command)

    def __onBeginConnectionManipulation(self):
        UndoRedoManager.getInstance().openBracket('Connect Ports')

    def __onEndConnectionManipulationSignal(self):
        UndoRedoManager.getInstance().closeBracket()

    def __onConnectionAdded(self, connection):
        if not UndoRedoManager.getInstance().isUndoingOrRedoing():
            command = graph_commands.ConnectionAddedCommand(self.graphView, self.guideRig, connection)
            UndoRedoManager.getInstance().addCommand(command)

    def __onConnectionRemoved(self, connection):
        if not UndoRedoManager.getInstance().isUndoingOrRedoing():
            command = graph_commands.ConnectionRemovedCommand(self.graphView, self.guideRig, connection)
            UndoRedoManager.getInstance().addCommand(command)

    def __onSelectionChanged(self, deselectedNodes, selectedNodes):
        if not UndoRedoManager.getInstance().isUndoingOrRedoing():
            command = graph_commands.SelectionChangeCommand(self.graphView, deselectedNodes, selectedNodes)
            UndoRedoManager.getInstance().addCommand(command)

    def __onSelectionMoved(self, nodes, delta):
        if not UndoRedoManager.getInstance().isUndoingOrRedoing():
            command = graph_commands.NodesMoveCommand(self.graphView, nodes, delta)
            UndoRedoManager.getInstance().addCommand(command)

    def __onBeginDeleteSelection(self):
        UndoRedoManager.getInstance().openBracket('Delete Nodes')

    def __onEndDeleteSelection(self):
        UndoRedoManager.getInstance().closeBracket()