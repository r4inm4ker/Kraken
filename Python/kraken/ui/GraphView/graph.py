

from PySide import QtGui, QtCore

from node import Node
from connection import Connection
from main_panel import MainPanel
from kraken.core.maths import Vec2
from kraken.core.kraken_system import KrakenSystem

class Graph(QtGui.QGraphicsWidget):

    def __init__(self, parent, rig):
        super(Graph, self).__init__()
        self.setObjectName('graphWidget')

        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))
        parentSize = parent.size()
        self.setMinimumSize(parentSize.width(), parentSize.height())

        self.__parent = parent
        self.__rig = rig
        self.__scene = QtGui.QGraphicsScene()
        self.__scene.addItem(self)

        self.__nodes = {}
        self.__connections = {}
        self.__selection = []

        self.__mainPanel = MainPanel(self)

        layout = QtGui.QGraphicsLinearLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addItem(self.__mainPanel)
        self.setLayout(layout)

        self.displayGraph()

    def graphView(self):
        return self.__parent


    def scene(self):
        return self.__scene

    def itemGroup(self):
        return self.__mainPanel.itemGroup()


    def getRig(self):
        return self.__rig

    #####################
    ## Nodes

    def addNode(self, component):
        node = Node(self, component)
        self.__nodes[node.getName()] = node
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
            # names += (" " + node.getName())
            component = node.getComponent()
            self.__rig.removeChild( component )

            node.destroy()
            del self.__nodes[node.getName()]

    def frameNodes(self, nodes):
        if len(nodes) == 0:
            return

        def computeWindowFrame():
            windowRect = self.mapRectToItem(self.itemGroup(), self.windowFrameGeometry())
            windowRect.setLeft(windowRect.left() + 16)
            windowRect.setRight(windowRect.right() - 16)
            windowRect.setTop(windowRect.top() + 16)
            windowRect.setBottom(windowRect.bottom() - 16)
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

        # Update the main panel when reframing.
        self.__mainPanel.update()

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

    def getConnections(self):
        return self.__connections

    def addConnection(self, source, target):

        key = source +">" + target
        if key in self.__connections:
            raise Exception("Error adding connection:" + key+ ". Graph already has a connection between the specified ports.")

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
        connection.setPortConnection(sourcePort)
        connection.setPortConnection(targetPort)

        self.__connections[key] = connection

    def removeConnection(self, source, target):

        key = source +">" + target
        if key not in self.__connections:
            raise Exception("Error removeing connection:" + key+ ". Graph does not have a connection between the specified ports.")
        connection = self.__connections[key]
        connection.destroy()
        del self.__connections[key]

    #######################
    ## Graph
    def displayGraph(self):
        self.clear()

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


    def clear(self):

        for connectionName, connection in self.__connections.iteritems():
            connection.destroy()
        for nodeName, node in self.__nodes.iteritems():
            node.destroy()

        self.__connections = {}
        self.__nodes = {}
        self.__selection = []

    #######################
    ## Copy/Paste

    def copySettings(self, pos):
        nodes = self.getSelectedNodes()
        clipboardData = {}

        copiedComponents = []
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


    def pasteSettings(self, clipboardData, pos):
        krakenSystem = KrakenSystem.getInstance()
        delta = pos - clipboardData['copyPos']
        self.clearSelection()
        pastedComponents = {}
        for componentData in clipboardData['components']:
            componentClass = krakenSystem.getComponentClass(componentData['class'])
            component = componentClass(parent=self.__rig)
            component.pasteData(componentData)
            graphPos = component.getGraphPos( )
            component.setGraphPos(Vec2(graphPos.x + delta.x(), graphPos.y + delta.y()))
            node = self.addNode(component)
            self.selectNode(node, False)

            # save a dict of the nodes using the orignal names
            pastedComponents[componentData['name'] + component.getNameDecoration()] = component

        for connectionData in clipboardData['connections']:
            sourceComponentDecoratedName, outputName = connectionData['source'].split('.')
            targetComponentDecoratedName, inputName = connectionData['target'].split('.')

            sourceComponent = None

            # The connection is either between nodes that were pasted, or from pasted nodes
            # to unpasted nodes. We first check that the source component is in the pasted group
            # else use the node in the graph.
            if sourceComponentDecoratedName in pastedComponents:
                sourceComponent = pastedComponents[sourceComponentDecoratedName]
            else:
                # When we support copying/pasting between rigs, then we may not find the source
                # node in the target rig.
                if sourceComponentDecoratedName not in self.getNodes().keys():
                    continue
                node = self.getNodes()[sourceComponentDecoratedName]
                sourceComponent = node.getComponent()

            targetComponent = pastedComponents[targetComponentDecoratedName]

            outputPort = sourceComponent.getOutputByName(outputName)
            inputPort = targetComponent.getInputByName(inputName)

            inputPort.setConnection(outputPort)
            self.addConnection(
                source = sourceComponent.getDecoratedName() + '.' + outputPort.getName(),
                target = targetComponent.getDecoratedName() + '.' + inputPort.getName()
            )


    #######################
    ## Events
    def closeEvent(self, event):
        return super(Graph, self).closeEvent(event)
