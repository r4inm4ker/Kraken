
#
# Copyright 2010-2015
#

from PySide import QtGui, QtCore
import json, difflib
from node import Node, NodeTitle, NodeHeader
from port import BasePort
from connection import Connection
# from FabricEngine.DFG.Widgets.add_port_dialog import AddPortDialog
# from FabricEngine.DFG.Widgets.dfg_function_editor import DFGFunctionEditorDockWidget
# from FabricEngine.DFG.Widgets.node_inspector import NodeInspectorDockWidget



class SelectionRect(QtGui.QGraphicsWidget):
    __backgroundColor = QtGui.QColor(100, 100, 100, 50)
    __pen =  QtGui.QPen(QtGui.QColor(25, 25, 25), 1.0,  QtCore.Qt.DashLine)

    def __init__(self, parent, mouseDownPos):
        super(SelectionRect, self).__init__(parent)
        self.setZValue(-1)

        # self.__parent = parent
        self.__mouseDownPos = mouseDownPos
        self.setPos(self.__mouseDownPos)
        self.resize(0, 0)

    def setDragPoint(self, dragPoint):
        topLeft = QtCore.QPointF(self.__mouseDownPos)
        bottomRight = QtCore.QPointF(dragPoint)
        if dragPoint.x() < self.__mouseDownPos.x():
            topLeft.setX(dragPoint.x())
            bottomRight.setX(self.__mouseDownPos.x())
        if dragPoint.y() < self.__mouseDownPos.y():
            topLeft.setY(dragPoint.y())
            bottomRight.setY(self.__mouseDownPos.y())
        self.setPos(topLeft)
        self.resize(bottomRight.x() - topLeft.x(), bottomRight.y() - topLeft.y())


    def paint(self, painter, option, widget):
        rect = self.windowFrameRect()
        painter.setBrush(self.__backgroundColor)
        painter.setPen(self.__pen)
        painter.drawRect(rect)


class MainPanel(QtGui.QGraphicsWidget):
    __backgroundColor = QtGui.QColor(50, 50, 50)
    __gridPenS = QtGui.QPen(QtGui.QColor(44, 44, 44, 255), 0.5)
    __gridPenL = QtGui.QPen(QtGui.QColor(40, 40, 40, 255), 1.0)
    __gridPenA = QtGui.QPen(QtGui.QColor(30, 30, 30, 255), 2.0)

    __mouseWheelZoomRate = 0.001

    def __init__(self, graph):
        super(MainPanel, self).__init__(graph)

        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))
        self.setAcceptDrops(True)

        self.graph = graph
        self.__itemGroup = QtGui.QGraphicsWidget(self)

        self._manipulationMode = 0
        self._dragging = False
        self._selectionRect = None

    def itemGroup(self):
        return self.__itemGroup

    def mousePressEvent(self, event):
        if event.button() is QtCore.Qt.MouseButton.LeftButton:
            mouseDownPos = self.mapToItem(self.graph.itemGroup(), event.pos())
            self._selectionRect = SelectionRect(self.__itemGroup, mouseDownPos)
            self._dragging = False
            self._manipulationMode = 1
        elif event.button() is QtCore.Qt.MouseButton.MiddleButton:
            self.setCursor(QtCore.Qt.OpenHandCursor)
            self._manipulationMode = 2
            self._lastPanPoint = event.pos()
        else:
            super(MainPanel, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._manipulationMode == 1:
            dragPoint = self.mapToItem(self.graph.itemGroup(), event.pos())
            self._selectionRect.setDragPoint(dragPoint)
            self.graph.clearSelection()
            for name, node in self.graph.getNodes().iteritems():
                if not node.isSelected() and self._selectionRect.collidesWithItem(node):
                    self.graph.selectNode(node)
            self._dragging = True

        elif self._manipulationMode == 2:
            (xfo, invRes) = self.__itemGroup.transform().inverted()
            delta = xfo.map(event.pos()) - xfo.map(self._lastPanPoint)
            self._lastPanPoint = event.pos()
            self.__itemGroup.translate(delta.x(), delta.y())
        else:
            super(MainPanel, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self._manipulationMode == 1:
            self.scene().removeItem(self._selectionRect)
            if not self._dragging:
                self.graph.clearSelection()
            self._selectionRect = None
            self._manipulationMode = 0
        elif self._manipulationMode == 2:
            self.setCursor(QtCore.Qt.ArrowCursor)
            self._manipulationMode = 0
        else:
            super(MainPanel, self).mouseReleaseEvent(event)

    def wheelEvent(self, event):

        (xfo, invRes) = self.__itemGroup.transform().inverted()
        topLeft = xfo.map(self.rect().topLeft())
        bottomRight = xfo.map(self.rect().bottomRight())
        center = ( topLeft + bottomRight ) * 0.5

        zoomFactor = 1.0 + event.delta() * self.__mouseWheelZoomRate
        transform = self.__itemGroup.transform()
        transform.scale(zoomFactor, zoomFactor)

        if transform.m22() > 0.01: # To avoid negative scalling as it would flip the graph
            self.__itemGroup.setTransform(transform)

            (xfo, invRes) = transform.inverted()
            topLeft = xfo.map(self.rect().topLeft())
            bottomRight = xfo.map(self.rect().bottomRight())
            newcenter = ( topLeft + bottomRight ) * 0.5

            # Re-center the graph on the old position.
            self.__itemGroup.translate(newcenter.x() - center.x(), newcenter.y() - center.y())

    def paint(self, painter, option, widget):
        # return super(MainPanel, self).paint(painter, option, widget)

        rect = self.__itemGroup.mapRectFromParent(self.windowFrameRect())

        oldTransform = painter.transform()
        painter.setTransform(self.__itemGroup.transform(), True)

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

        painter.setTransform(oldTransform)

        return super(MainPanel, self).paint(painter, option, widget)


class ContextualNodeList(QtGui.QWidget):

    class NodeList(QtGui.QListWidget):

        def __init__(self, parent, controller):
            # constructors of base classes
            QtGui.QListWidget.__init__(self, parent)

            def getNodeList(path):
                nodes = []
                desc = controller.getDesc(path=path)
                if desc['objectType'] == 'namespace':
                    for namespace in desc['namespaces']:
                        if path == "":
                            namespacePath = namespace['name']
                        else:
                            namespacePath = path+"."+namespace['name']
                        nodes = nodes + getNodeList(namespacePath)

                elif desc['objectType'] == 'function' or desc['objectType'] == 'graph':
                    nodes.append(desc['path'])

                return nodes

            self.allNodes = getNodeList('')
            self.installEventFilter(self)

        def eventFilter(self, object, event):
            if event.type()== QtCore.QEvent.WindowDeactivate:
                self.parent().hide()
                return True
            elif event.type()== QtCore.QEvent.FocusOut:
                self.parent().hide()
                return True
            return False

    def __init__(self, parent, controller, graph):
        super(ContextualNodeList, self).__init__(parent)

        self.controller = controller
        self.graph = graph
        self.setFixedSize(250, 200)

        self.searchLineEdit = QtGui.QLineEdit(parent)
        self.searchLineEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.searchLineEdit.setFocus()

        self.nodesList = ContextualNodeList.NodeList(self, controller)

        grid = QtGui.QGridLayout()
        grid.addWidget(self.searchLineEdit, 0, 0)
        grid.addWidget(self.nodesList, 1, 0)
        self.setLayout(grid)

        self.nodes = None
        self.showClosestNames()
        self.searchLineEdit.textEdited.connect(self.showClosestNames)
        self.nodesList.itemClicked.connect(self.createNode)

    def showAtPos(self, pos, graphpos):
        posx = pos.x() - self.width() * 0.1
        self.move(posx, pos.y() - 20)
        self.pos = pos
        self.graphpos = graphpos
        self.searchLineEdit.setFocus()
        self.searchLineEdit.clear()
        self.nodesList.clear()
        self.show()

    def createNode(self):
        if self.nodesList.currentItem() is not None:
            executablePath = self.nodesList.currentItem().text()

            # Add a node to the graph at the given position.
            self.controller.addNode(
                graphPath=self.graph.getGraphPath(),
                executablePath=executablePath,
                graphPos=self.graphpos
            )

    def showClosestNames(self):
        self.nodesList.clear()
        fuzzyText = self.searchLineEdit.text()
        if fuzzyText == '':
            matches = self.nodesList.allNodes
            matches.sort()
        else:
            matches = difflib.get_close_matches(fuzzyText, self.nodesList.allNodes, n=10, cutoff=0.2)

        for m in matches:
            self.nodesList.addItem(QtGui.QListWidgetItem(m))
        self.setIndex(0)

    def setIndex(self, index):
        if index >= 0:
            self.index = index
            self.nodesList.setCurrentItem(self.nodesList.item(self.index))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            if self.isVisible():
                self.hide()

        elif event.key() == QtCore.Qt.Key_Up or event.key() == QtCore.Qt.Key_Down:
            if event.key() == QtCore.Qt.Key_Up:
                self.setIndex(self.index-1)
            elif event.key() == QtCore.Qt.Key_Down:
                self.setIndex(self.index+1)

        elif event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
            if self.isVisible():
                self.createNode()
                self.hide()

        return False


class ContextualNewNodeWidget(QtGui.QWidget):

    def __init__(self, parent, controller, graph, objectType, pos):
        super(ContextualNewNodeWidget, self).__init__(parent)

        self.controller = controller
        self.graph = graph
        self.objectType = objectType
        # self.setFixedSize(350, 300)

        defaultPath = '.'.join(self.graph.getGraphPath().split('.')[0:-1]) + "."

        self.searchLineEdit = QtGui.QLineEdit(parent)
        self.searchLineEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.searchLineEdit.setFocus()
        self.searchLineEdit.installEventFilter(self)
        self.searchLineEdit.setText(defaultPath)

        grid = QtGui.QGridLayout()
        grid.addWidget(self.searchLineEdit, 0, 0)
        self.setLayout(grid)

        posx = pos.x() - self.width() * 0.1
        self.move(posx, pos.y())
        self.pos = pos
        self.show()

    def eventFilter(self, object, event):
        if event.type()== QtCore.QEvent.WindowDeactivate:
            self.close()
            return True
        elif event.type()== QtCore.QEvent.FocusOut:
            self.close()
            return True
        return False

    def createNode(self):
        executablePath = self.searchLineEdit.text()

        if self.objectType == 'graph':
            nodes = self.graph.getSelectedNodes()
            names = ""
            nodePaths = []
            for node in nodes:
                names += (" " + node.getName())
                nodePaths.append(node.getNodePath())
            self.controller.beginInteraction("Create Graph from nodes:"+ str(names));
            self.graph.clearSelection()
            newGraphPath = self.controller.newGraphNode(
                executablePath=executablePath,
                graphPath=self.graph.getGraphPath(),
                graphPos=QtCore.QPointF(self.pos.x() - 40, self.pos.y() + 20),
                nodePaths=nodePaths
            )
        elif self.objectType == 'function':

            self.controller.beginInteraction("Create Node");
            # Note: newFunctionNode might midfy the path by inserting 'Fabric' at the begining (Hack to be removed ASAP)
            executablePath = self.controller.newFunctionNode(
                executablePath=executablePath
            )

            # Add a node to the graph at the given position.
            self.controller.addNode(
                graphPath=self.graph.getGraphPath(),
                executablePath=executablePath,
                graphPos=QtCore.QPointF(self.pos.x() - 40, self.pos.y() + 20)
            )

        self.controller.endInteraction()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            if self.isVisible():
                self.close()

        if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
            if self.isVisible():
                self.createNode()
                self.close()
            return True

class Graph(QtGui.QGraphicsWidget):

    def __init__(self, parent, rig):
        super(Graph, self).__init__()

        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))
        self.setMinimumSize(400, 400)

        self.__parent = parent
        self.__rig = rig
        self.__scene = QtGui.QGraphicsScene()
        self.__scene.addItem(self)

        self.__nodes = {}
        self.__connections = {}
        self.__selection = []

        self.__mainPanel = MainPanel(self)

        self.setContentsMargins(2, 0, 2, 0)
        layout = QtGui.QGraphicsLinearLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addItem(self.__mainPanel)
        self.setLayout(layout)

        # self.__controller.addNotificationListener('port.created', self.__portCreated)
        # self.__controller.addNotificationListener('port.destroyed', self.__portDestroyed)
        # self.__controller.addNotificationListener('node.created', self.__nodeCreated)
        # self.__controller.addNotificationListener('node.destroyed', self.__nodeDestroyed)
        # self.__controller.addNotificationListener('graph.connected', self.__connectionAdded)
        # self.__controller.addNotificationListener('graph.disconnected', self.__connectionRemoved)
        # self.__controller.addNotificationListener('graph.metadata.changed', self.graphMetadataChanged)
        # self.__controller.addNotificationListener('scene.new', self.__onSceneChange)
        # self.__controller.addNotificationListener('scene.load', self.__onSceneChange)
        # self.__controller.addNotificationListener('scene.bindingChanged', self.__bindingChanged)

        self.displayGraph()

    def getName(self):
        return self.__name

    def scene(self):
        return self.__scene

    def itemGroup(self):
        return self.__mainPanel.itemGroup()

    # def controller(self):
    #     return self.__controller

    def getGraphPath(self):
        return self.graphPath

    def getEvalPath(self):
        return self.__evalPath

    def getDisplayedEvalPath(self):
        evalPathStr = self.__controller.getRootEvalPath()
        for lvl in self.__evalPath:
            evalPathStr += '.' + str(lvl)
        return evalPathStr


    #####################
    ## Nodes

    def addNode(self, component):
        node = Node(self, component)
        self.__nodes[component.getName()] = node
        return node

    def getNode(self, name):
        if name in self.__nodes:
            return self.__nodes[name]
        return None

    def getNodes(self):
        return self.__nodes

    def clearSelection(self):
        for node in self.__selection:
            node.setSelected(False)
        self.__selection = []

    def selectNode(self, node):
        node.setSelected(True)
        self.__selection.append(node)

    def getSelectedNodes(self):
        return self.__selection

    def deleteSelectedNodes(self):
        selectedNodes = self.getSelectedNodes()
        names = ""
        for node in selectedNodes:
            names += (" " + node.getName())
        self.__controller.beginInteraction("Delete " + names)
        for node in selectedNodes:
            self.__controller.removeNode(nodePath=node.getNodePath())
        self.__controller.endInteraction()

    def frameNodes(self, nodes):
        if len(nodes) == 0:
            return;

        def computeWindowFrame():
            windowRect = self.mapRectToItem(self.itemGroup(), self.windowFrameGeometry())
            # leftSidePanelRect = self.mapRectToItem(self.itemGroup(), self.__leftPanel.windowFrameGeometry())
            # rightSidePanelRect = self.mapRectToItem(self.itemGroup(), self.__rightPanel.windowFrameGeometry())
            # windowRect.setLeft(leftSidePanelRect.right() + 8)
            # windowRect.setRight(rightSidePanelRect.left() - 8)
            # windowRect.setTop(windowRect.top() + 8)
            # windowRect.setBottom(windowRect.bottom() - 8)
            return windowRect

        nodesRect = None
        for node in nodes:
            nodeRect = self.mapToScene(node.transform().map(node.rect())).boundingRect()
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

        transform = self.itemGroup().transform()
        transform.scale(scale, scale)
        if transform.m11() > 1.0 or transform.m22() > 1.0:
            transform.scale(1.0/transform.m11(), 1.0/transform.m22())
        self.itemGroup().setTransform(transform)

        # After zooming, recompute the window boundaries and compute the pan.
        windowRect = computeWindowFrame()
        pan = windowRect.center() - nodesRect.center()
        self.itemGroup().translate(pan.x(), pan.y())

    def frameSelectedNodes(self):
        self.frameNodes(self.getSelectedNodes())

    def frameAllNodes(self):
        allnodes = []
        for name, node in self.__nodes.iteritems():
            allnodes.append(node)
        self.frameNodes(allnodes)

    # def createGraphFromSelectedNodes(self):
    #     nodes = self.getSelectedNodes()
    #     for name, node in self.__nodes.iteritems():
    #         allnodes.append(node)
    #     self.frameNodes(allnodes)

    def __nodeCreated(self, event):
        graphPath = '.'.join(event['node']['path'].split('.')[0:-1])
        if graphPath == self.graphPath:
            self.addNode(event['node']['name'])

    def __nodeDestroyed(self, event):
        graphPath = '.'.join(event['node']['path'].split('.')[0:-1])
        if graphPath == self.graphPath:
            name = event['node']['path'].split('.')[-1]
            if name not in self.__nodes:
                raise Exception("Error removeing node:" + name+ ". Graph does not have a node of the given name.")
            node = self.__nodes[name]
            node.destroy()
            del self.__nodes[name]

    #######################
    ## Connections

    def addConnection(self, connectionDef):

        # remove the graph path from the start of the string to get the graph relative path.
        source = connectionDef['source']
        target = connectionDef['target']

        key = source +">" + target
        if key in self.__connections:
            raise Exception("Error adding connection:" + key+ ". Graph already has a connection between the specified ports.")

        sourceComponent, outputName = tuple(source.split('.'))
        targetComponent, inputName = tuple(target.split('.'))

        #     sourceNodeName = sourcePath[0]
        sourceNode = self.getNode(sourceComponent)
        if not sourceNode:
            raise Exception("Component not found:" + sourceNodeName)

        sourcePort = sourceNode.getPort(outputName)
        if not sourcePort:
            raise Exception("Component '"+sourceNodeName+"'' does not have output:" + sourcePortName)

        targetNode = self.getNode(targetComponent)
        if not targetNode:
            raise Exception("Component not found:" + targetNodeName)

        targetPort = targetNode.getPort(inputName)
        if not targetPort:
            raise Exception("Component '"+targetNodeName+"'' does not have input:" + targetPortName)

        connection = Connection(self, sourcePort, targetPort)
        self.__connections[key] = connection

    def removeConnection(self, source, target):

        # remove the graph path from the start of the string to get the graph relative path.
        source = source[len(self.graphPath)+1:]
        target = target[len(self.graphPath)+1:]

        key = source +">" + target
        if key not in self.__connections:
            raise Exception("Error removeing connection:" + key+ ". Graph does not have a connection between the specified ports.")
        connection = self.__connections[key]
        connection.destroy();
        del self.__connections[key]

    def __connectionAdded(self, data):
        # fired when a connection is connected
        # {u'src.port': {u'path': u'Scene.Root.foo'}, u'dst.pin': {u'path': u'Scene.Root.Add.lhs'}, u'desc': u'graph.connected'}
        if ('src.port' in data and data['src.port']['path'].startswith(self.graphPath)) and ('dst.port' in data and data['dst.port']['path'].startswith(self.graphPath)):
            self.addConnection(data['src.port']['path'], data['dst.port']['path'])
        elif ('src.pin' in data and data['src.pin']['path'].startswith(self.graphPath)) and ('dst.port' in data and data['dst.port']['path'].startswith(self.graphPath)):
            self.addConnection(data['src.pin']['path'], data['dst.port']['path'])
        elif ('src.port' in data and data['src.port']['path'].startswith(self.graphPath)) and ('dst.pin' in data and data['dst.pin']['path'].startswith(self.graphPath)):
            self.addConnection(data['src.port']['path'], data['dst.pin']['path'])
        elif ('src.pin' in data and data['src.pin']['path'].startswith(self.graphPath)) and ('dst.pin' in data and data['dst.pin']['path'].startswith(self.graphPath)):
            self.addConnection(data['src.pin']['path'], data['dst.pin']['path'])

    def __connectionRemoved(self, data):
        # fired when a connection is disconnected
        if ('src.port' in data and data['src.port']['path'].startswith(self.graphPath)) and ('dst.port' in data and data['dst.port']['path'].startswith(self.graphPath)):
            self.removeConnection(data['src.port']['path'], data['dst.port']['path'])
        elif ('src.pin' in data and data['src.pin']['path'].startswith(self.graphPath)) and ('dst.port' in data and data['dst.port']['path'].startswith(self.graphPath)):
            self.removeConnection(data['src.pin']['path'], data['dst.port']['path'])
        elif ('src.port' in data and data['src.port']['path'].startswith(self.graphPath)) and ('dst.pin' in data and data['dst.pin']['path'].startswith(self.graphPath)):
            self.removeConnection(data['src.port']['path'], data['dst.pin']['path'])
        elif ('src.pin' in data and data['src.pin']['path'].startswith(self.graphPath)) and ('dst.pin' in data and data['dst.pin']['path'].startswith(self.graphPath)):
            self.removeConnection(data['src.pin']['path'], data['dst.pin']['path'])

    #######################
    ## Graph

    def pushSubGraph(self, subGraphName):
        self.__evalPath.append(subGraphName)
        self.displayGraph()

    def popSubGraph(self):
        self.__evalPath = self.__evalPath[:-1]
        self.displayGraph()

    def displayGraph(self):
        self.clear()

        guideComponents = self.__rig.getChildrenByType('Component')

        # {"name":"AddGraph","types":["SInt32","SInt32","SInt32"]}
        for component in guideComponents:
            self.addNode(component)


        for component in guideComponents:
            for i in range(component.getNumInputs()):
                componentInput = component.getInputByIndex(i)
                if componentInput.isConnected():
                    componentOutput = componentInput.getConnection()
                    connectionJson = {
                        'source': componentOutput.getParent().getName() + '.' + componentOutput.getName(),
                        'target': component.getName() + '.' + componentInput.getName()
                    }
                    self.addConnection(connectionJson)

        self.frameAllNodes()


    def clear(self):

        for connectionName, connection in self.__connections.iteritems():
            connection.destroy()
        for nodeName, node in self.__nodes.iteritems():
            node.destroy()

        self.__connections = {}
        self.__nodes = {}
        self.__selection = []


    #######################
    ## Functions

    def openEditFunctionDialog(self, evalPath, executablePath):
        self.__parent.openEditFunctionDialog(evalPath, executablePath)

    #######################
    ## Events

    def __bindingChanged(self, data):
        self.__evalDesc = self.__controller.getDescForEvalPath(evalPath=self.__evalPath)

    def graphMetadataChanged(self, data):
        if 'graph' in data and data['graph']['path'] == self.graphPath:
            if data['graph']['metadata'] != "":
                pass
                # metadata = json.loads(data['graph']['metadata'])

    def __onSceneChange(self, data):
        self.__evalPath = []
        self.displayGraph()


    def closeEvent(self, event):
        self.__controller.removeNotificationListener('scene.bindingChanged', self.__bindingChanged)

        return super(Graph, self).closeEvent(event)


class GraphView(QtGui.QGraphicsView):
    def __init__(self, rig, parent=None):
        super(GraphView, self).__init__(parent)

        self.rig = rig
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setRenderHint(QtGui.QPainter.TextAntialiasing)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.setResizeAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        # self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        # self.setContentsMargins(0, 0, 0, 0)

        self.graph = Graph(self, rig)
        self.setScene(self.graph.scene())

        self.setAcceptDrops(True)


    ################################################
    ## Graph
    def getGraph(self):
        return self.graph

    def popSubGraph(self):
        self.graph.popSubGraph()

    def getDisplayedEvalPath(self):
        return self.graph.getDisplayedEvalPath()

    def frameSelectedNodes(self):
        self.graph.frameSelectedNodes()

    def frameAllNodes(self):
        self.graph.frameAllNodes()

    def deleteSelectedNodes(self):
        self.graph.deleteSelectedNodes()


    ################################################
    ## Function

    def openEditFunctionDialog(self, evalPath, executablePath):
        DFGFunctionEditorDockWidget.showWidget(self.__controller, evalPath, executablePath, floating=True)

    ################################################
    ## Ports

    def openAddPortDialog(self, graphPath, evalPath, portType=None):
        addPortDialog = AddPortDialog(self, self.__controller, evalPath=evalPath, executablePath=graphPath, portType=portType)
        addPortDialog.show()

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
        print "dragEnterEvent:" + event.mimeData().text()
        textParts = event.mimeData().text().split(':')
        if textParts[0] == 'KrakenComponent':
            event.accept()
        else:
            event.setDropAction(QtCore.Qt.IgnoreAction)
            super(GraphView, self).dragEnterEvent(event)
            #event.setDropAction(QtCore.Qt.IgnoreAction)

    def dragMoveEvent(self, event):
        super(GraphView, self).dragMoveEvent(event)
        event.accept()

    def dropEvent(self, event):
        textParts = event.mimeData().text().split(':')
        if textParts[0] == 'DFGNode':
            executablePath = textParts[1]

            # Add a node to the graph at the given position.
            dropPosition = self.graph.mapToItem(self.graph.itemGroup(), event.pos())
            self.__controller.addNode(
                graphPath=self.graph.getGraphPath(),
                executablePath=executablePath,
                graphPos=dropPosition
            )

            event.acceptProposedAction()
        else:
            super(GraphView, self).dropEvent(event)

    def resizeEvent(self, event):
        self.graph.resize(event.size())

    def closeEvent(self, event):

        self.__controller.removeNotificationListener('port.created', self.__portCreated)
        self.__controller.removeNotificationListener('port.destroyed', self.__portDestroyed)
        self.__controller.removeNotificationListener('node.created', self.__nodeCreated)
        self.__controller.removeNotificationListener('node.destroyed', self.__nodeDestroyed)
        self.__controller.removeNotificationListener('graph.connected', self.__connectionAdded)
        self.__controller.removeNotificationListener('graph.disconnected', self.__connectionRemoved)
        self.__controller.removeNotificationListener('graph.metadata.changed', self.graphMetadataChanged)
        self.__controller.removeNotificationListener('scene.new', self.__onSceneChange)
        self.__controller.removeNotificationListener('scene.load', self.__onSceneChange)

        return super(GraphView, self).closeEvent(event)

    def saveExecutable(self):
        self.__controller.saveExecutable(executablePath=self.graph.getGraphPath())


class GraphViewWidget(QtGui.QWidget):

    def __init__(self, rig, parent=None):

        # constructors of base classes
        super(GraphViewWidget, self).__init__(parent)

        self.setAcceptDrops(True)

        self.graphView = GraphView(rig, self)
        self.__contextualNodeList = None

        # setup the toobar
        toolBar = QtGui.QToolBar()

        newAction = toolBar.addAction('New')
        # newAction.setShortcut('Ctrl+S')
        # newAction.triggered.connect(self.graphView.saveExecutable)
        newAction.setObjectName("saveButton")

        saveAction = toolBar.addAction('Save')
        # saveAction.setShortcut('Ctrl+S')
        # saveAction.triggered.connect(self.graphView.saveExecutable)
        saveAction.setObjectName("saveButton")

        loadAction = toolBar.addAction('Load')
        # loadAction.setShortcut('Ctrl+S')
        # loadAction.triggered.connect(self.graphView.saveExecutable)
        saveAction.setObjectName("saveButton")

        toolBar.addSeparator()

        toolBar.addWidget(QtGui.QLabel('Name:'))
        nameWidget = QtGui.QLineEdit('', self)
        toolBar.addWidget(nameWidget)


        # deleteAction = toolBar.addAction('Delete')
        # deleteAction.setShortcut(QtGui.QKeySequence.Delete)
        # deleteAction.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete))
        # deleteAction.triggered.connect(self.graphView.deleteSelectedNodes)

        toolBar.addSeparator()

        buildGuideAction = toolBar.addAction('Build Guide')
        # buildGuideAction.triggered.connect(self.graphView.popSubGraph)

        buildGuideAction = toolBar.addAction('Build Rig')
        # buildGuideAction.triggered.connect(self.graphView.popSubGraph)

        # frameAction = toolBar.addAction('Frame Selected Nodes')
        # frameAction.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F))
        # # frameAction.triggered.connect(self.graphView.frameSelectedNodes)

        # frameAction = toolBar.addAction('Frame All  Nodes')
        # frameAction.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_A))
        # # frameAction.triggered.connect(self.graphView.frameAllNodes)

        # def inspectGraph():
        #     NodeInspectorDockWidget.showWidget(controller, self.graphView.getGraph().getEvalPath(), self.graphView.getGraph().getGraphPath(), floating=True)
        # inspectAction = toolBar.addAction('Inspect')
        # inspectAction.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_I))
        # inspectAction.triggered.connect(inspectGraph)


        # def updateWidgetsBasedOnEvalPath(evalPath):
        #     executionPathWidget.setText(str(evalPath))
        #     upAction.setEnabled(len(evalPath.split('.')) > 1)
        # self.graphView.getGraph().evalPathChanged.connect(updateWidgetsBasedOnEvalPath)
        # updateWidgetsBasedOnEvalPath(self.graphView.getDisplayedEvalPath())

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(toolBar)
        layout.addWidget(self.graphView)

        self.setLayout(layout)


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

    def dragEnterEvent(self, event):
        print "GraphViewWidget.dragEnterEvent:" + event.mimeData().text()
