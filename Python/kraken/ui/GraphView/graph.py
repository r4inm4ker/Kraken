

from PySide import QtGui, QtCore

from node import Node
from connection import Connection

from main_panel import MainPanel

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
            # names += (" " + node.getName())
            component = node.getComponent()
            self.__rig.removeChild( component )

            node.destroy()
            del self.__nodes[node.getName()]



        # self.__controller.beginInteraction("Delete " + names)
        # for node in selectedNodes:
        #     self.__controller.removeNode(nodePath=node.getNodePath())
        # self.__controller.endInteraction()

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

        sourcePort = sourceNode.getOutPort(outputName)
        if not sourcePort:
            raise Exception("Component '"+sourceNodeName+"'' does not have output:" + sourcePortName)

        targetNode = self.getNode(targetComponent)
        if not targetNode:
            raise Exception("Component not found:" + targetNodeName)

        targetPort = targetNode.getInPort(inputName)
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
    ## Events

    def closeEvent(self, event):
        return super(Graph, self).closeEvent(event)