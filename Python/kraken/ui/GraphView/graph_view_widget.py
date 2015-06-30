import json, difflib
import os.path

from PySide import QtGui, QtCore

from kraken.ui.GraphView.contextual_node_list import ContextualNodeList, ContextualNewNodeWidget
from kraken.ui.GraphView.graph_view import GraphView

from kraken.core.objects.rig import Rig
from kraken import plugins


def GetHomePath():
    homeDir = os.path.expanduser("~")
    return homeDir


class GraphViewWidget(QtGui.QWidget):

    def __init__(self, parent=None):

        # constructors of base classes
        super(GraphViewWidget, self).__init__(parent)
        self.setObjectName('graphViewWidget')
        self.setAttribute(QtCore.Qt.WA_WindowPropagation, True)

        self.graphView = GraphView(parent=self)
        self.__contextualNodeList = None

        # setup the toobar
        toolBar = QtGui.QToolBar()
        toolBar.setObjectName('mainToolbar')


        logoWidget = QtGui.QLabel()
        logoWidget.setObjectName('logoWidget')
        logoWidget.setMinimumHeight(20)
        logoWidget.setMinimumWidth(97)

        logoPixmap = QtGui.QPixmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'images', 'KrakenUI_Logo.png'))
        logoWidget.setPixmap(logoPixmap)
        toolBar.addWidget(logoWidget)

        newAction = toolBar.addAction('New')
        newAction.setShortcut('Ctrl+N')
        newAction.triggered.connect(self.newRigPreset)
        newAction.setObjectName("newButton")

        saveAction = toolBar.addAction('Save')
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.saveRigPreset)
        saveAction.setObjectName("saveButton")

        loadAction = toolBar.addAction('Load')
        loadAction.setShortcut('Ctrl+S')
        loadAction.triggered.connect(self.loadRigPreset)
        saveAction.setObjectName("loadButton")

        toolBar.addSeparator()

        # Setup the name widget
        rigNameLabel = QtGui.QLabel('Rig Name:')
        rigNameLabel.setObjectName('rigNameLabel')
        toolBar.addWidget(rigNameLabel)
        self.nameWidget = QtGui.QLineEdit('', self)

        self.nameWidget.textChanged.connect(self.setRigName)
        toolBar.addWidget(self.nameWidget)

        toolBar.addSeparator()

        buildGuideAction = toolBar.addAction('Build Guide')
        buildGuideAction.triggered.connect(self.buildGuideRig)

        buildGuideAction = toolBar.addAction('Build Rig')
        buildGuideAction.triggered.connect(self.buildRig)

        #########################
        ## Setup hotkeys for the following actions.
        deleteShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete), self)
        deleteShortcut.activated.connect(self.graphView.deleteSelectedNodes)

        frameShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F), self)
        frameShortcut.activated.connect(self.graphView.frameSelectedNodes)

        frameShortcut = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_A), self)
        frameShortcut.activated.connect(self.graphView.frameAllNodes)

        # Setup Layout
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(toolBar)
        layout.addWidget(self.graphView)

        self.setLayout(layout)

        self.newRigPreset()

    def getContextualNodeList(self):
        return self.__contextualNodeList

    def setRigName(self, text):
        self.guideRig.setName(text)

    def newRigPreset(self):
        # TODO: clean the rig from the scene if it has been built.
        self.guideRig = Rig()
        self.graphView.init(self.guideRig)
        self.nameWidget.setText('MyRig')

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
            self.graphView.init( self.guideRig )
            self.nameWidget.setText( self.guideRig.getName() )

    def buildGuideRig(self):
        builder = plugins.getBuilder()

        if self.guideRig.getName().endswith('_guide') is False:
            self.guideRig.setName(self.guideRig.getName() + '_guide')

        builder.build(self.guideRig)

    def synchGuideRig(self):
        synchronizer = plugins.getSynchronizer()
        synchronizer.setTarget(self.guideRig)
        synchronizer.sync()

    def buildRig(self):
            self.synchGuideRig()

            rigBuildData = self.guideRig.getRigBuildData()
            rig = Rig()
            rig.loadRigDefinition(rigBuildData)

            rig.setName(rig.getName().replace('_guide', ''))

            builder = plugins.getBuilder()
            builder.build(rig)

    # =======
    # Events
    # =======
    def keyPressEvent(self, event):

        modifiers = event.modifiers()
        if event.key() == 96: #'`'
            pos = self.mapFromGlobal(QtGui.QCursor.pos());
            if not self.__contextualNodeList:
                self.__contextualNodeList = ContextualNodeList(self)
            else:
                # Ensures that the node list is reset to list all components
                self.__contextualNodeList.showClosestNames()

            scenepos = self.graphView.getGraph().mapToScene(pos)
            self.__contextualNodeList.showAtPos(pos, scenepos, self.graphView.getGraph())

        # Ctrl+W
        elif event.key() == 87 and modifiers == QtCore.Qt.ControlModifier:
            self.window().close()

        # Ctrl+N
        elif event.key() == 78 and modifiers == QtCore.Qt.ControlModifier:
            self.newRigPreset()

        # Ctrl+C
        elif event.key() == 67 and modifiers == QtCore.Qt.ControlModifier:
            graph = self.graphView.getGraph()
            pos = graph.getSelectedNodesPos()
            self.graphView.__class__._clipboardData = graph.copySettings(pos)

        # Ctrl+V
        elif event.key() == 86 and modifiers == QtCore.Qt.ControlModifier:
            graph = self.graphView.getGraph()
            clipboardData = self.graphView.__class__._clipboardData

            pos = clipboardData['copyPos'] + QtCore.QPoint(20, 20)
            graph.pasteSettings(clipboardData, pos, createConnectionsToExistingNodes=False)

        # Ctrl+Shift+V
        elif event.key() == 86 and modifiers == (QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier):
            graph = self.graphView.getGraph()
            clipboardData = self.graphView.__class__._clipboardData

            pos = clipboardData['copyPos'] + QtCore.QPoint(20, 20)
            graph.pasteSettings(clipboardData, pos)

        # Tab
        elif event.key() == QtCore.Qt.Key_Tab and modifiers == QtCore.Qt.ControlModifier:
            splitter = self.parentWidget()
            sizes = splitter.sizes()

            if sizes[0] == 0:
                splitter.setSizes([175, sizes[1]])
            else:
                splitter.setSizes([0, sizes[1]])