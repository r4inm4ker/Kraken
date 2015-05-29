
#
# Copyright 2010-2015
#

import json, difflib
import os.path
from PySide import QtGui, QtCore

from kraken.core.maths import Vec2

from kraken.core.objects.rig import Rig
from kraken.core.kraken_system import KrakenSystem

from contextual_node_list import ContextualNodeList, ContextualNewNodeWidget
from graph import Graph


class GraphView(QtGui.QGraphicsView):
    def __init__(self, parent=None):
        super(GraphView, self).__init__(parent)

        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setRenderHint(QtGui.QPainter.TextAntialiasing)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.setResizeAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        # self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        # self.setContentsMargins(0, 0, 0, 0)

        self.setAcceptDrops(True)

    ################################################
    ## Graph
    def init(self, rig):
        self.rig = rig
        self.graph = Graph(self, rig)
        self.setScene(self.graph.scene())


    ################################################
    ## Graph
    def getGraph(self):
        return self.graph

    def frameSelectedNodes(self):
        self.graph.frameSelectedNodes()

    def frameAllNodes(self):
        self.graph.frameAllNodes()

    def deleteSelectedNodes(self):
        self.graph.deleteSelectedNodes()

    ################################################
    ## Events

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            def __getGraphItem(graphicItem):
                if isinstance(graphicItem, Node):
                    return graphicItem
                if isinstance(graphicItem, SidePanelPort):
                    return graphicItem
                if isinstance(graphicItem, ProxySidePanelPort):
                    return graphicItem
                elif isinstance(graphicItem, MainPanel):
                    return graphicItem
                elif(isinstance(graphicItem, QtGui.QGraphicsTextItem) or
                     isinstance(graphicItem, NodeTitle) or
                     isinstance(graphicItem, NodeHeader) or
                     isinstance(graphicItem, PortLabel) or
                     isinstance(graphicItem, PortFromPath)):
                    return __getGraphItem(graphicItem.parentItem())
                return None
            pos = self.getGraph().mapToScene(event.pos())
            graphicItem = __getGraphItem(self.itemAt(int(pos.x()), int(pos.y())))
            contextMenu = QtGui.QMenu(self.__dfgEditor)

            if isinstance(graphicItem, MainPanel):
                def newGraphNode():
                    ContextualNewNodeWidget(self, self.__controller, self.getGraph(), 'graph', pos)
                contextMenu.addAction("New Graph Node").triggered.connect(newGraphNode)
                def newFunctionNode():
                    ContextualNewNodeWidget(self, self.__controller, self.getGraph(), 'function', pos)
                contextMenu.addAction("New Function Node").triggered.connect(newFunctionNode)

            elif isinstance(graphicItem, ProxySidePanelPort):
                connectionPointType = graphicItem.getSidePanel().getConnectionPortType()
                if connectionPointType == 'In':
                    portType = 'Out'
                elif connectionPointType == 'Out':
                    portType = 'In'
                else:
                    portType = connectionPointType
                def addPort():
                    self.openAddPortDialog(graphPath=self.graph.getGraphPath(), evalPath=self.graph.getEvalPath(), portType=portType)
                contextMenu.addAction("Add Port").triggered.connect(addPort)

            elif isinstance(graphicItem, SidePanelPort):
                def editPort():
                    print "EditPort"
                contextMenu.addAction("Edit Port").triggered.connect(editPort)
                def removePort():
                    self.__controller.removePort(executablePath=self.graph.getGraphPath(), evalPath=self.graph.getEvalPath(), portName=graphicItem.getName())
                contextMenu.addAction("Remove Port").triggered.connect(removePort)

            elif isinstance(graphicItem, Node):
                def newGraph():
                    ContextualNewNodeWidget(self, self.__controller, self.getGraph(), 'graph', pos)
                contextMenu.addAction("New Graph Node").triggered.connect(newGraph)
            contextMenu.popup(event.globalPos())

        else:
            super(GraphView, self).mousePressEvent(event)

    def dragEnterEvent(self, event):
        textParts = event.mimeData().text().split(':')
        if textParts[0] == 'KrakenComponent':
            event.accept()
        else:
            event.setDropAction(QtCore.Qt.IgnoreAction)
            super(GraphView, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        super(GraphView, self).dragMoveEvent(event)
        event.accept()

    def dropEvent(self, event):
        textParts = event.mimeData().text().split(':')
        if textParts[0] == 'KrakenComponent':
            componentClassName = textParts[1]

            # Add a component to the rig placed at the given position.
            dropPosition = self.graph.mapToItem(self.graph.itemGroup(), event.pos())

            ##############################
            ## construct

            krakenSystem = KrakenSystem.getInstance()
            componentClass = krakenSystem.getComponentClass( componentClassName )
            component = componentClass(parent=self.rig)
            component.setGraphPos( Vec2(dropPosition.x(), dropPosition.y()) )

            self.graph.addNode(component)

            event.acceptProposedAction()
        else:
            super(GraphView, self).dropEvent(event)

    def resizeEvent(self, event):
        self.graph.resize(event.size())

    def closeEvent(self, event):

        # self.__controller.removeNotificationListener('port.created', self.__portCreated)
        # self.__controller.removeNotificationListener('port.destroyed', self.__portDestroyed)
        # self.__controller.removeNotificationListener('node.created', self.__nodeCreated)
        # self.__controller.removeNotificationListener('node.destroyed', self.__nodeDestroyed)
        # self.__controller.removeNotificationListener('graph.connected', self.__connectionAdded)
        # self.__controller.removeNotificationListener('graph.disconnected', self.__connectionRemoved)
        # self.__controller.removeNotificationListener('graph.metadata.changed', self.graphMetadataChanged)
        # self.__controller.removeNotificationListener('scene.new', self.__onSceneChange)
        # self.__controller.removeNotificationListener('scene.load', self.__onSceneChange)

        return super(GraphView, self).closeEvent(event)

def GetHomePath():
    from os.path import expanduser
    homeDir = expanduser("~")
    return homeDir

class GraphViewWidget(QtGui.QWidget):

    def __init__(self, parent=None):

        # constructors of base classes
        super(GraphViewWidget, self).__init__(parent)

        self.graphView = GraphView(parent=self)
        self.__contextualNodeList = None

        # setup the toobar
        toolBar = QtGui.QToolBar()

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
        toolBar.addWidget(QtGui.QLabel('Name:'))
        self.nameWidget = QtGui.QLineEdit('', self)
        def setRigName( text ):
            self.rig.setName( text )
        self.nameWidget.textChanged.connect(setRigName)
        toolBar.addWidget( self.nameWidget )

        toolBar.addSeparator()

        buildGuideAction = toolBar.addAction('Build Guide')
        buildGuideAction.triggered.connect(self.buildGuideRig)

        buildGuideAction = toolBar.addAction('Build Rig')
        buildGuideAction.triggered.connect(self.buildRig)

        #########################
        ## TODO: Setup hotkeys for the following actions.

        # deleteAction = toolBar.addAction('Delete')
        # deleteAction.setShortcut(QtGui.QKeySequence.Delete)
        # deleteAction.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete))
        # deleteAction.triggered.connect(self.graphView.deleteSelectedNodes)

        # frameAction = toolBar.addAction('Frame Selected Nodes')
        # frameAction.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F))
        # # frameAction.triggered.connect(self.graphView.frameSelectedNodes)

        # frameAction = toolBar.addAction('Frame All  Nodes')
        # frameAction.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_A))
        # # frameAction.triggered.connect(self.graphView.frameAllNodes)

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(toolBar)
        layout.addWidget(self.graphView)

        self.setLayout(layout)

        self.newRigPreset()

    def newRigPreset(self):
        # TODO: clean the rig from the scene if it has been built.
        self.rig = Rig()
        self.graphView.init( self.rig )
        self.nameWidget.setText( 'MyRig' )

    def saveRigPreset(self):
        lastSceneFilePath = os.path.join(GetHomePath(), self.rig.getName() )
        (filePath, filter) = QtGui.QFileDialog.getSaveFileName(self, 'Save Rig Preset', lastSceneFilePath, 'Kraken Rig (*.krg)')
        if len(filePath) > 0:
            self.rig.writeGuideDefinitionFile(filePath)

    def loadRigPreset(self):
        lastSceneFilePath = GetHomePath()
        (filePath, filter) = QtGui.QFileDialog.getOpenFileName(self, 'Load Rig Preset', lastSceneFilePath, 'Kraken Rig (*.krg)')
        if len(filePath) > 0:
            self.rig = Rig()
            self.rig.loadRigDefinitionFile(filePath)
            self.graphView.init( self.rig )
            self.nameWidget.setText( self.rig.getName() )

    def buildGuideRig(self):
        print 'buildGuideRig'

    def buildRig(self):
        print 'buildRig'

    def keyPressEvent(self, event):
        if event.key() == 96: #'`'
            pos = self.mapFromGlobal(QtGui.QCursor.pos());
            if not self.__contextualNodeList:
                self.__contextualNodeList = ContextualNodeList(self, self.__controller, self.graphView.getGraph())


            scenepos = self.graphView.getGraph().mapToScene(pos)

            # xfo = self.graphView.getGraph().itemGroup().transform()
            # scenepos = xfo.map(pos)
            # print "pos:" + str(pos)
            # print "scenepos:" + str(scenepos)
            self.__contextualNodeList.showAtPos(pos, scenepos)

