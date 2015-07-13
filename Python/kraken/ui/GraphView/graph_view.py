#
# Copyright 2010-2015
#
import copy

import json, difflib
import os.path

from PySide import QtGui, QtCore
# from graph import Graph
from node import Node, NodeTitle
from port import PortLabel, InputPort, OutputPort

from selection_rect import SelectionRect

from kraken.ui.undoredo.undo_redo_manager import UndoRedoManager
from graph_commands import ConstructComponentCommand, SelectionChangeCommand

from kraken.core.maths import Vec2
from kraken.core.kraken_system import KrakenSystem


class GraphView(QtGui.QGraphicsView):

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
        # self.graph = None

        # self.__nodes = {}
        # self.__connections = {}
        # self.__selection = []


        # self.__scene = QtGui.QGraphicsScene()
        # self.setScene(self.__scene)

        # self.__itemGroup = QtGui.QGraphicsWidget()
        # self.__scene.addItem(self.__itemGroup)

        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setRenderHint(QtGui.QPainter.TextAntialiasing)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # self.setResizeAnchor(QtGui.QGraphicsView.NoAnchor)
        # self.setTransformationAnchor(QtGui.QGraphicsView.NoAnchor)

        self.resize(600, 400)
        self.setSceneRect(-300, -200, 600, 400)

        self.setAcceptDrops(True)
        self.reset()


    # def itemGroup(self):
    #     return self.__itemGroup
        
    def getGraphViewWidget(self):
        return self.__graphViewWidget


    def getRig(self):
        return self.__rig

    ################################################
    ## Graph
    def reset(self):
        self.__scene = QtGui.QGraphicsScene()
        # self.__itemGroup = QtGui.QGraphicsWidget()
        # self.__scene.addItem(self.__itemGroup)
        self.setScene(self.__scene)

        self.__connections = {}
        self.__nodes = {}
        self.__selection = []

        self._manipulationMode = 0
        self._dragging = False
        self._selectionRect = None
        self._selectionchanged = False

        self.__rig = None

    ################################################
    ## Graph

    #####################
    ## Nodes

    def addNode(self, component):
        node = Node(self, component)
        self.scene().addItem(node)
        self.__nodes[node.getName()] = node
        return node

    def removeNode(self, node):
        component = node.getComponent()
        self.__rig.removeChild( component )
        node.destroy()
        del self.__nodes[node.getName()]

    def getNode(self, name):
        if name in self.__nodes:
            return self.__nodes[name]
        return None

    def getNodes(self):
        return self.__nodes

    def nodeNameChanged(self, origName, newName ):
        if newName in self.__nodes and self.__nodes[origName] != self.__nodes[newName]:
            raise Exception("New name collides with existing node.")
        node = self.__nodes[origName]
        self.__nodes[newName] = node
        del self.__nodes[origName]

    def clearSelection(self):
        for node in self.__selection:
            node.setSelected(False)
        self.__selection = []

    def selectNode(self, node, clearSelection=False):
        if clearSelection is True:
            self.clearSelection()

        if node in self.__selection:
            raise IndexError("Node is already in selection!")

        node.setSelected(True)

        self.__selection.append(node)

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
            # windowRect = self.mapRectToItem(self.itemGroup(), self.windowFrameGeometry())
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

        scaleX = windowRect.width() / nodesRect.width()
        scaleY = windowRect.height() / nodesRect.height()
        if scaleY > scaleX:
            scale = scaleX
        else:
            scale = scaleY

        transform = self.transform()
        transform.scale(scale, scale)
        if transform.m11() > 1.0 or transform.m22() > 1.0:
            transform.scale(1.0/transform.m11(), 1.0/transform.m22())
        self.setTransform(transform)

        # After zooming, recompute the window boundaries and compute the pan.
        windowRect = computeWindowFrame()
        pan = windowRect.center() - nodesRect.center()
        print "pan:" + str(pan)
        self.translate(pan.x(), pan.y())

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

    def addConnection(self, source, target):

        sourceComponent, outputName = tuple(source.split('.'))
        targetComponent, inputName = tuple(target.split('.'))
        sourceNode = self.getNode(sourceComponent)
        if not sourceNode:
            raise Exception("Component not found:" + sourceNode.getName())

        sourcePort = sourceNode.getOutPort(outputName)
        if not sourcePort:
            raise Exception("Component '" + sourceNode.getName() + "' does not have output:" + sourcePort.getName())


        targetNode = self.getNode(targetComponent)
        if not targetNode:
            raise Exception("Component not found:" + targetNode.getName())

        targetPort = targetNode.getInPort(inputName)
        if not targetPort:
            raise Exception("Component '" + targetNode.getName() + "' does not have input:" + targetPort.getName())

        connection = Connection(self, sourcePort, targetPort)
        sourcePort.addConnection(connection)
        targetPort.addConnection(connection)

        return connection

    #######################
    ## Graph
    def displayGraph(self, rig):
        self.reset()

        self.__rig = rig

        guideComponents = self.__rig.getChildrenByType('Component')

        for component in guideComponents:
            self.addNode(component)

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
    # def mousePressEvent(self, event):
    #     print "GraphView.mousePressEvent"
    #     if event.button() == QtCore.Qt.MouseButton.RightButton:

    #         def __getGraphItem(graphicItem):
    #             if isinstance(graphicItem, Node):
    #                 return graphicItem
    #             elif(isinstance(graphicItem, QtGui.QGraphicsTextItem) or
    #                  isinstance(graphicItem, NodeTitle) or
    #                  isinstance(graphicItem, OutputPort) or
    #                  isinstance(graphicItem, InputPort)):
    #                 return __getGraphItem(graphicItem.parentItem())
    #             return None

    #         pos = self.getGraph().mapToScene(event.pos())
    #         graphicItem = __getGraphItem(self.itemAt(int(pos.x()), int(pos.y())))

    #         if graphicItem is None:

    #             if self.__class__._clipboardData is not None:

    #                 contextMenu = QtGui.QMenu(self.__graphViewWidget)
    #                 contextMenu.setObjectName('rightClickContextMenu')
    #                 contextMenu.setMinimumWidth(150)

    #                 def pasteSettings():
    #                     self.graph.pasteSettings(self.__class__._clipboardData, pos)

    #                 def pasteSettingsMirrored():
    #                     self.graph.pasteSettings(self.__class__._clipboardData, pos, mirrored=True)

    #                 contextMenu.addAction("Paste").triggered.connect(pasteSettings)
    #                 contextMenu.addAction("Paste Mirrored").triggered.connect(pasteSettingsMirrored)
    #                 contextMenu.popup(event.globalPos())


    #         if isinstance(graphicItem, Node) and graphicItem.isSelected():
    #             contextMenu = QtGui.QMenu(self.__graphViewWidget)
    #             contextMenu.setObjectName('rightClickContextMenu')
    #             contextMenu.setMinimumWidth(150)

    #             def copySettings():
    #                 self.__class__._clipboardData = self.graph.copySettings(pos)

    #             contextMenu.addAction("Copy").triggered.connect(copySettings)

    #             if self.__class__._clipboardData is not None:

    #                 def pasteSettings():
    #                     # Paste the settings, not modifying the location, because that will be used to determine symmetry.
    #                     graphicItem.getComponent().pasteData(self.__class__._clipboardData['components'][0], setLocation=False)

    #                 contextMenu.addSeparator()
    #                 contextMenu.addAction("Paste Data").triggered.connect(pasteSettings)

    #             contextMenu.popup(event.globalPos())

    #     elif event.button() == QtCore.Qt.MouseButton.LeftButton:

    #         graphViewWidget = self.parent()
    #         contextualNodeList = graphViewWidget.getContextualNodeList()
    #         if contextualNodeList is not None and contextualNodeList.isVisible():
    #             contextualNodeList.searchLineEdit.clear()
    #             contextualNodeList.hide()

    #         else:

    #             super(GraphView, self).mousePressEvent(event)

    #     else:
    #         super(GraphView, self).mousePressEvent(event)

    def mousePressEvent(self, event):
        if event.button() is QtCore.Qt.MouseButton.LeftButton:
            mouseDownPos = self.mapToScene(event.pos())
            self._selectionRect = SelectionRect(parent=None, mouseDownPos=mouseDownPos)
            self.scene().addItem(self._selectionRect)
            self._dragging = False
            self._manipulationMode = 1
            self._mouseDownSelection = copy.copy(self.getSelectedNodes())

        elif event.button() is QtCore.Qt.MouseButton.MiddleButton:
            self.setCursor(QtCore.Qt.OpenHandCursor)
            self._manipulationMode = 2
            self._lastPanPoint = self.mapToScene(event.pos())
            print "GraphView.mousePressEvent self._lastPanPoint:" + str(self._lastPanPoint)

        # else:
        #     super(GraphView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._manipulationMode == 1:
            dragPoint = self.mapToScene(event.pos())
            self._selectionRect.setDragPoint(dragPoint)
            self.clearSelection()
            for name, node in self.getNodes().iteritems():
                if not node.isSelected() and self._selectionRect.collidesWithItem(node):
                    self.selectNode(node)
                    self._selectionchanged = True
            self._dragging = True


        elif self._manipulationMode == 2:
            # (xfo, invRes) = self.__itemGroup.transform().inverted()
            # delta = xfo.map(event.pos()) - xfo.map(self._lastPanPoint)
            delta = self.mapToScene(event.pos()) - self._lastPanPoint
            print "GraphView.mouseMoveEvent _manipulationMode = 2 delta:" + str(delta)

            self.translate(delta.x(), delta.y())
            self._lastPanPoint = self.mapToScene(event.pos())

            # Call udpate to redraw background
            self.update()
        # else:
        #     print "super(GraphView, self).mouseMoveEvent(event)"
        #     super(GraphView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self._manipulationMode == 1:
            self.scene().removeItem(self._selectionRect)
            if not self._dragging:
                self.clearSelection()
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

            command = SelectionChangeCommand(self, selectedNodes, deselectedNodes)
            UndoRedoManager.getInstance().addCommand(command, invokeRedoOnAdd=False)

        elif self._manipulationMode == 2:
            self.setCursor(QtCore.Qt.ArrowCursor)
            self._manipulationMode = 0

        # else:
        #     super(Graph, self).mouseReleaseEvent(event)

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

        transform.scale(zoomFactor, zoomFactor)

        if transform.m22() > 0.01: # To avoid negative scalling as it would flip the graph
            self.setTransform(transform)

            (xfo, invRes) = transform.inverted()
            topLeft = xfo.map(self.rect().topLeft())
            bottomRight = xfo.map(self.rect().bottomRight())
            newcenter = ( topLeft + bottomRight ) * 0.5

        #     # Re-center the graph on the old position.
        #     transform = self.transform()
            transform.translate(newcenter.x() - center.x(), newcenter.y() - center.y())
            self.setTransform(transform)

        self.resize(self.size())

        # Call udpate to redraw background
        self.update()

    def resizeEvent(self, event):
        size = event.size()
        self.setSceneRect(-300, -200, size.width(), size.height())
        # self.graph.resize(event.size())

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
            # dropPosition = self.itemGroup().mapFromParent(event.pos())
            dropPosition = self.mapToScene(event.pos())

            # construct
            command = ConstructComponentCommand(self, componentClassName, Vec2(dropPosition.x(), dropPosition.y()))
            UndoRedoManager.getInstance().addCommand(command, invokeRedoOnAdd=True)

            event.acceptProposedAction()
        else:
            super(GraphView, self).dropEvent(event)


    def closeEvent(self, event):
        return super(GraphView, self).closeEvent(event)

    ################################################
    ## Painting

    def drawBackground(self, painter, rect):

        # rect = self.__itemGroup.mapRectFromParent(self.windowFrameRect())

        oldTransform = painter.transform()
        # painter.setTransform(self.__itemGroup.transform(), True)

        painter.fillRect(rect, self.__backgroundColor)
        painter.setTransform(self.transform(), True)

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

        painter.setTransform(oldTransform)

        return super(GraphView, self).drawBackground(painter, rect)

