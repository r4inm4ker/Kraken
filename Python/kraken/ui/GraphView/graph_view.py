#
# Copyright 2010-2015
#

import json, difflib
import os.path

from PySide import QtGui, QtCore
from graph import Graph
from node import Node, NodeTitle
from port import PortLabel

from kraken.core.maths import Vec2
from kraken.core.kraken_system import KrakenSystem


class GraphView(QtGui.QGraphicsView):

    def __init__(self, parent=None):
        super(GraphView, self).__init__(parent)
        self.setObjectName('graphView')

        self.__graphViewWidget = parent
        self.rig = None
        self.graph = None

        self.resize(600, 400)

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

    def getGraphViewWidget(self):
        return self.__graphViewWidget

    def getGraph(self):
        return self.graph


    ################################################
    ## Graph
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

            return

            def __getGraphItem(graphicItem):
                if isinstance(graphicItem, Node):
                    return graphicItem
                elif isinstance(graphicItem, MainPanel):
                    return graphicItem
                elif(isinstance(graphicItem, QtGui.QGraphicsTextItem) or
                     isinstance(graphicItem, NodeTitle) or
                     isinstance(graphicItem, PortLabel)):
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

        elif event.button() == QtCore.Qt.MouseButton.LeftButton:

            graphViewWidget = self.parent()
            contextualNodeList = graphViewWidget.getContextualNodeList()
            if contextualNodeList is not None and contextualNodeList.isVisible():
                contextualNodeList.searchLineEdit.clear()
                contextualNodeList.hide()

            else:
                super(GraphView, self).mousePressEvent(event)

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
        return super(GraphView, self).closeEvent(event)
