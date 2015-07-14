#
# Copyright 2010-2015
#
import copy

import json, difflib
import os.path

from PySide import QtGui, QtCore
# from graph import Graph
from node import Node, NodeTitle
from port import BasePort, PortLabel, InputPort, OutputPort
from connection import Connection

from selection_rect import SelectionRect

from kraken.ui.undoredo.undo_redo_manager import UndoRedoManager
from kraken.ui.GraphView.graph_commands import ConstructComponentCommand, SelectionChangeCommand

from kraken.core.maths import Vec2
from kraken.core.kraken_system import KrakenSystem


class GraphView(QtGui.QGraphicsView):

    nodeAdded = QtCore.Signal(Node)
    nodeRemoved = QtCore.Signal(Node)

    beginConnectionManipulation = QtCore.Signal()
    endConnectionManipulation = QtCore.Signal()
    connectionAdded = QtCore.Signal(Connection)
    connectionRemoved = QtCore.Signal(Connection)

    selectionChanged = QtCore.Signal(list, list)
    selectionMoved = QtCore.Signal(QtCore.QPointF)

    _clipboardData = None


    __backgroundColor = QtGui.QColor(50, 50, 50)
    __gridPenS = QtGui.QPen(QtGui.QColor(44, 44, 44, 255), 0.5)
    __gridPenL = QtGui.QPen(QtGui.QColor(40, 40, 40, 255), 1.0)
    __gridPenA = QtGui.QPen(QtGui.QColor(30, 30, 30, 255), 2.0)

    __mouseWheelZoomRate = 0.0005

    def __init__(self, parent=None):
        super(GraphView, self).__init__(parent)
        self.setObjectName('graphView')

        self.__graphViewWidget = parent

        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setRenderHint(QtGui.QPainter.TextAntialiasing)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # Explicitly set the scene rect. This ensures all view parameters will be explicitly controlled
        # in the event handlers of this class. 
        size = QtCore.QSize(600, 400);
        self.resize(size)
        self.setSceneRect(-size.width() * 0.5, -size.height() * 0.5, size.width(), size.height())

        self.setAcceptDrops(True)
        self.reset()

        
    def getGraphViewWidget(self):
        return self.__graphViewWidget


    def getRig(self):
        return self.__rig

    ################################################
    ## Graph
    def reset(self):
        self.setScene(QtGui.QGraphicsScene())

        self.__connections = set()
        self.__nodes = {}
        self.__selection = set()

        self._manipulationMode = 0
        self._selectionRect = None

        self.__rig = None

    ################################################
    ## Graph

    #####################
    ## Nodes

    def addNode(self, node, emitNotification=True):
        self.scene().addItem(node)
        self.__nodes[node.getName()] = node

        if emitNotification:
            self.nodeAdded.emit(node)

        return node

    def removeNode(self, node, emitNotification=True):
        del self.__nodes[node.getName()]
        self.scene().removeItem(node)

        if emitNotification:
            self.nodeRemoved.emit(node)

    def getNode(self, name):
        if name in self.__nodes:
            return self.__nodes[name]
        return None


    def nodeNameChanged(self, origName, newName ):
        if newName in self.__nodes and self.__nodes[origName] != self.__nodes[newName]:
            raise Exception("New name collides with existing node.")
        node = self.__nodes[origName]
        self.__nodes[newName] = node
        del self.__nodes[origName]


    def clearSelection(self):
        for node in self.__selection:
            node.setSelected(False)
        self.__selection.clear()

    def selectNode(self, node, clearSelection=False):
        if clearSelection is True:
            self.clearSelection()

        if node in self.__selection:
            raise IndexError("Node is already in selection!")

        node.setSelected(True)

        self.__selection.add(node)

    def deselectNode(self, node):

        node.setSelected(False)

        if node not in self.__selection:
            raise IndexError("Node is not in selection!")

        self.__selection.remove(node)

    def getSelectedNodes(self):
        return self.__selection


    def deleteSelectedNodes(self):
        selectedNodes = self.getSelectedNodes()
        names = ""
        for node in selectedNodes:
            self.removeNode(node)


    def frameNodes(self, nodes):
        if len(nodes) == 0:
            return

        def computeWindowFrame():
            windowRect = self.rect()
            windowRect.setLeft(windowRect.left() + 16)
            windowRect.setRight(windowRect.right() - 16)
            windowRect.setTop(windowRect.top() + 16)
            windowRect.setBottom(windowRect.bottom() - 16)
            return windowRect

        nodesRect = None
        for node in nodes:
            nodeRectF = node.transform().mapRect(node.rect())
            nodeRect = QtCore.QRect(nodeRectF.x(), nodeRectF.y(), nodeRectF.width(), nodeRectF.height())
            if nodesRect is None:
                nodesRect = nodeRect
            else:
                nodesRect = nodesRect.united(nodeRect)


        windowRect = computeWindowFrame()

        scaleX = float(windowRect.width()) / float(nodesRect.width())
        scaleY = float(windowRect.height()) / float(nodesRect.height())
        if scaleY > scaleX:
            scale = scaleX
        else:
            scale = scaleY

        if scale < 1.0:
            self.setTransform(QtGui.QTransform.fromScale(scale, scale))
        else:
            self.setTransform(QtGui.QTransform())

        sceneRect = self.sceneRect()
        pan = sceneRect.center() - nodesRect.center()
        sceneRect.translate(-pan.x(), -pan.y())
        self.setSceneRect(sceneRect)

        # Update the main panel when reframing.
        self.update()


    def frameSelectedNodes(self):
        self.frameNodes(self.getSelectedNodes())

    def frameAllNodes(self):
        allnodes = []
        for name, node in self.__nodes.iteritems():
            allnodes.append(node)
        self.frameNodes(allnodes)

    def getSelectedNodesPos(self):
        selectedNodes = self.getSelectedNodes()

        leftMostNode = None
        topMostNode = None
        for node in selectedNodes:
            nodePos = node.getGraphPos()

            if leftMostNode is None:
                leftMostNode = node
            else:
                if nodePos.x() < leftMostNode.getGraphPos().x():
                    leftMostNode = node

            if topMostNode is None:
                topMostNode = node
            else:
                if nodePos.y() < topMostNode.getGraphPos().y():
                    topMostNode = node

        xPos = leftMostNode.getGraphPos().x()
        yPos = topMostNode.getGraphPos().y()
        pos = QtCore.QPoint(xPos, yPos)

        return pos

    #######################
    ## Connections

    # def addConnection(self, source, target):

    #     sourceComponent, outputName = tuple(source.split('.'))
    #     targetComponent, inputName = tuple(target.split('.'))
    #     sourceNode = self.getNode(sourceComponent)
    #     if not sourceNode:
    #         raise Exception("Component not found:" + sourceNode.getName())

    #     sourcePort = sourceNode.getOutPort(outputName)
    #     if not sourcePort:
    #         raise Exception("Component '" + sourceNode.getName() + "' does not have output:" + sourcePort.getName())


    #     targetNode = self.getNode(targetComponent)
    #     if not targetNode:
    #         raise Exception("Component not found:" + targetNode.getName())

    #     targetPort = targetNode.getInPort(inputName)
    #     if not targetPort:
    #         raise Exception("Component '" + targetNode.getName() + "' does not have input:" + targetPort.getName())

    #     connection = Connection(self, sourcePort, targetPort)
    #     sourcePort.addConnection(connection)
    #     targetPort.setConnection(connection)

    #     self.connectionAdded.emit(connection)

    #     return connection

    def emitBeginConnectionManipulationSignal(self):
        self.beginConnectionManipulation.emit()


    def emitEndConnectionManipulationSignal(self):
        self.endConnectionManipulation.emit()


    def addConnection(self, connection, emitNotification=True):

        self.__connections.add(connection)
        self.scene().addItem(connection)
        if emitNotification:
            self.connectionAdded.emit(connection)
        return connection

    def removeConnection(self, connection, emitNotification=True):

        connection.disconnect()
        self.__connections.remove(connection)
        self.scene().removeItem(connection)
        if emitNotification:
            self.connectionRemoved.emit(connection)

    #######################
    ## Graph
    def displayGraph(self, rig):
        self.reset()

        self.__rig = rig

        guideComponents = self.__rig.getChildrenByType('Component')

        for component in guideComponents:
            self.addNode(Node(self,component))

        for component in guideComponents:
            for i in range(component.getNumInputs()):
                componentInput = component.getInputByIndex(i)
                if componentInput.isConnected():
                    componentOutput = componentInput.getConnection()
                    self.addConnection(
                        source = componentOutput.getParent().getDecoratedName() + '.' + componentOutput.getName(),
                        target = component.getDecoratedName() + '.' + componentInput.getName()
                    )

        self.frameAllNodes()

    ################################################
    ## Events

    def mousePressEvent(self, event):

        # If the contextual node list is open, close it. 
        contextualNodeList = self.__graphViewWidget.getContextualNodeList()
        if contextualNodeList is not None and contextualNodeList.isVisible():
            contextualNodeList.searchLineEdit.clear()
            contextualNodeList.hide()

        if event.button() is QtCore.Qt.MouseButton.LeftButton and self.itemAt(event.pos()) is None:
            self._manipulationMode = 1
            self._mouseDownSelection = copy.copy(self.getSelectedNodes())
            self.clearSelection()
            self._selectionRect = SelectionRect(graph=self, mouseDownPos=self.mapToScene(event.pos()))

        elif event.button() is QtCore.Qt.MouseButton.MiddleButton:

            self.setCursor(QtCore.Qt.OpenHandCursor)
            self._manipulationMode = 2
            self._lastPanPoint = self.mapToScene(event.pos())

        elif event.button() == QtCore.Qt.MouseButton.RightButton:

            def graphItemAt(item):
                if isinstance(item, Node):
                    return item
                elif(isinstance(item, QtGui.QGraphicsTextItem) or
                     isinstance(item, NodeTitle) or
                     isinstance(item, BasePort)):
                    return graphItemAt(item.parentItem())
                return None
            graphicItem = graphItemAt(self.itemAt(event.pos()))
            pos = self.mapToScene(event.pos())

            if graphicItem is None:

                if self.__class__._clipboardData is not None:

                    contextMenu = QtGui.QMenu(self.__graphViewWidget)
                    contextMenu.setObjectName('rightClickContextMenu')
                    contextMenu.setMinimumWidth(150)

                    def pasteSettings():
                        self.pasteSettings(self.__class__._clipboardData, pos)

                    def pasteSettingsMirrored():
                        self.pasteSettings(self.__class__._clipboardData, pos, mirrored=True)

                    contextMenu.addAction("Paste").triggered.connect(pasteSettings)
                    contextMenu.addAction("Paste Mirrored").triggered.connect(pasteSettingsMirrored)
                    contextMenu.popup(event.globalPos())


            if isinstance(graphicItem, Node) and graphicItem.isSelected():
                contextMenu = QtGui.QMenu(self.__graphViewWidget)
                contextMenu.setObjectName('rightClickContextMenu')
                contextMenu.setMinimumWidth(150)

                def copySettings():
                    self.__class__._clipboardData = self.copySettings(pos)

                contextMenu.addAction("Copy").triggered.connect(copySettings)

                if self.__class__._clipboardData is not None:

                    def pasteSettings():
                        # Paste the settings, not modifying the location, because that will be used to determine symmetry.
                        graphicItem.getComponent().pasteData(self.__class__._clipboardData['components'][0], setLocation=False)

                    contextMenu.addSeparator()
                    contextMenu.addAction("Paste Data").triggered.connect(pasteSettings)

                contextMenu.popup(event.globalPos())

        else:
            super(GraphView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._manipulationMode == 1:
            dragPoint = self.mapToScene(event.pos())
            self._selectionRect.setDragPoint(dragPoint)
            for name, node in self.__nodes.iteritems():
                if not node.isSelected() and self._selectionRect.collidesWithItem(node):
                    self.selectNode(node)

        elif self._manipulationMode == 2:
            delta = self.mapToScene(event.pos()) - self._lastPanPoint

            rect = self.sceneRect()
            rect.translate(-delta.x(), -delta.y())
            self.setSceneRect(rect)

            self._lastPanPoint = self.mapToScene(event.pos())

        elif self._manipulationMode == 3:

            newPos = self.mapToScene(event.pos())
            delta = newPos - self._lastDragPoint
            self._lastDragPoint = newPos

            selectedNodes = self.getSelectedNodes()

            # Apply the delta to each selected node
            for node in selectedNodes:
                node.translate(delta.x(), delta.y())

        else:
            super(GraphView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self._manipulationMode == 1:
            self._selectionRect.destroy()
            self._selectionRect = None
            self._manipulationMode = 0

            selection = self.getSelectedNodes()

            deselectedNodes = []
            selectedNodes = []

            for node in self._mouseDownSelection:
                if node not in selection:
                    deselectedNodes.append(node)

            for node in selection:
                if node not in self._mouseDownSelection:
                    selectedNodes.append(node)

            if selectedNodes != deselectedNodes:
                self.selectionChanged.emit(selectedNodes, deselectedNodes)

        elif self._manipulationMode == 2:
            self.setCursor(QtCore.Qt.ArrowCursor)
            self._manipulationMode = 0

        else:
            super(GraphView, self).mouseReleaseEvent(event)

    def wheelEvent(self, event):

        (xfo, invRes) = self.transform().inverted()
        topLeft = xfo.map(self.rect().topLeft())
        bottomRight = xfo.map(self.rect().bottomRight())
        center = ( topLeft + bottomRight ) * 0.5

        zoomFactor = 1.0 + event.delta() * self.__mouseWheelZoomRate

        transform = self.transform()

        # Limit zoom to 3x
        if transform.m22() * zoomFactor >= 2.0 or transform.m22() * zoomFactor <= 0.25:
            return

        self.scale(zoomFactor, zoomFactor)

        # Call udpate to redraw background
        self.update()


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
            dropPosition = self.mapToScene(event.pos())

            # construct the node and add it to the graph.
            krakenSystem = KrakenSystem.getInstance()
            componentClass = krakenSystem.getComponentClass( componentClassName )
            component = componentClass(parent=self.getRig())
            component.setGraphPos(Vec2(dropPosition.x(), dropPosition.y()))
            self.addNode(Node(self, component) )

            event.acceptProposedAction()
        else:
            super(GraphView, self).dropEvent(event)


    def closeEvent(self, event):
        return super(GraphView, self).closeEvent(event)

    ################################################
    ## Painting

    def drawBackground(self, painter, rect):

        oldTransform = painter.transform()
        painter.fillRect(rect, self.__backgroundColor)

        gridSize = 30
        left = int(rect.left()) - (int(rect.left()) % gridSize)
        top = int(rect.top()) - (int(rect.top()) % gridSize)

        # Draw horizontal fine lines
        gridLines = []
        painter.setPen(self.__gridPenS)
        y = float(top)
        while y < float(rect.bottom()):
            gridLines.append(QtCore.QLineF( rect.left(), y, rect.right(), y ))
            y += gridSize
        painter.drawLines(gridLines)

        # Draw vertical fine lines
        gridLines = []
        painter.setPen(self.__gridPenS)
        x = float(left)
        while x < float(rect.right()):
            gridLines.append(QtCore.QLineF( x, rect.top(), x, rect.bottom()))
            x += gridSize
        painter.drawLines(gridLines)

        # Draw thick grid
        gridSize = 30 * 10
        left = int(rect.left()) - (int(rect.left()) % gridSize)
        top = int(rect.top()) - (int(rect.top()) % gridSize)

        # Draw vertical thick lines
        gridLines = []
        painter.setPen(self.__gridPenL)
        x = left
        while x < rect.right():
            gridLines.append(QtCore.QLineF( x, rect.top(), x, rect.bottom() ))
            x += gridSize
        painter.drawLines(gridLines)

        # Draw horizontal thick lines
        gridLines = []
        painter.setPen(self.__gridPenL)
        y = top
        while y < rect.bottom():
            gridLines.append(QtCore.QLineF( rect.left(), y, rect.right(), y ))
            y += gridSize
        painter.drawLines(gridLines)

        return super(GraphView, self).drawBackground(painter, rect)

    #######################
    ## Copy/Paste

    def copySettings(self, pos):
        clipboardData = {}

        copiedComponents = []
        nodes = self.getSelectedNodes()
        for node in nodes:
            copiedComponents.append(node.getComponent())

        componentsJson = []
        connectionsJson = []
        for component in copiedComponents:
            componentsJson.append(component.copyData())

            for i in range(component.getNumInputs()):
                componentInput = component.getInputByIndex(i)
                if componentInput.isConnected():
                    componentOutput = componentInput.getConnection()
                    connectionJson = {
                        'source': componentOutput.getParent().getDecoratedName() + '.' + componentOutput.getName(),
                        'target': component.getDecoratedName() + '.' + componentInput.getName()
                    }

                    connectionsJson.append(connectionJson)

        clipboardData = {
            'components': componentsJson,
            'connections': connectionsJson,
            'copyPos': pos
        }

        return clipboardData

    def pasteSettings(self, clipboardData, pos, mirrored=False, createConnectionsToExistingNodes=True):

        krakenSystem = KrakenSystem.getInstance()
        delta = pos - clipboardData['copyPos']
        self.clearSelection()
        pastedComponents = {}
        nameMapping = {}

        for componentData in clipboardData['components']:
            componentClass = krakenSystem.getComponentClass(componentData['class'])
            component = componentClass(parent=self.__rig)
            decoratedName = componentData['name'] + component.getNameDecoration()
            nameMapping[decoratedName] = decoratedName
            if mirrored:
                config = Config.getInstance()
                mirrorMap = config.getNameTemplate()['mirrorMap']
                component.setLocation(mirrorMap[componentData['location']])
                nameMapping[decoratedName] = componentData['name'] + component.getNameDecoration()
                component.pasteData(componentData, setLocation=False)
            else:
                component.pasteData(componentData, setLocation=True)
            graphPos = component.getGraphPos( )
            component.setGraphPos(Vec2(graphPos.x + delta.x(), graphPos.y + delta.y()))
            node = Node(self,component)
            self.addNode(node)
            self.selectNode(node, False)

            # save a dict of the nodes using the orignal names
            pastedComponents[nameMapping[decoratedName]] = component


        for connectionData in clipboardData['connections']:
            sourceComponentDecoratedName, outputName = connectionData['source'].split('.')
            targetComponentDecoratedName, inputName = connectionData['target'].split('.')

            sourceComponent = None

            # The connection is either between nodes that were pasted, or from pasted nodes
            # to unpasted nodes. We first check that the source component is in the pasted group
            # else use the node in the graph.
            if sourceComponentDecoratedName in nameMapping:
                sourceComponent = pastedComponents[nameMapping[sourceComponentDecoratedName]]
            else:
                if not createConnectionsToExistingNodes:
                    continue;

                # When we support copying/pasting between rigs, then we may not find the source
                # node in the target rig.
                if sourceComponentDecoratedName not in self.__nodes.keys():
                    continue
                node = self.__nodes[sourceComponentDecoratedName]
                sourceComponent = node.getComponent()

            targetComponentDecoratedName = nameMapping[targetComponentDecoratedName]
            targetComponent = pastedComponents[targetComponentDecoratedName]

            outputPort = sourceComponent.getOutputByName(outputName)
            inputPort = targetComponent.getInputByName(inputName)

            inputPort.setConnection(outputPort)
            self.addConnection(
                source = sourceComponent.getDecoratedName() + '.' + outputPort.getName(),
                target = targetComponent.getDecoratedName() + '.' + inputPort.getName()
            )
