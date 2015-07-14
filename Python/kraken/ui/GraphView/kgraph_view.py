#
# Copyright 2010-2015
#

from PySide import QtGui, QtCore



from graph_view.graph_view import GraphView
from graph_view.node import Node, NodeTitle, PortList
from graph_view.port import BasePort, PortLabel, InputPort, OutputPort

from kraken.core.maths import Vec2
from kraken.core.kraken_system import KrakenSystem
from kraken.core.configs.config import Config

# from knode import KNode

class KGraphView(GraphView):
    
    _clipboardData = None

    def __init__(self, parent=None):
        super(KGraphView, self).__init__(parent)
        self.__rig = None
        self.setAcceptDrops(True)


    def getRig(self):
        return self.__rig

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
        contextualNodeList = self.getGraphViewWidget().getContextualNodeList()
        if contextualNodeList is not None and contextualNodeList.isVisible():
            contextualNodeList.searchLineEdit.clear()
            contextualNodeList.hide()

        if event.button() == QtCore.Qt.MouseButton.RightButton:

            def graphItemAt(item):
                if isinstance(item, Node):
                    return item
                elif item is not None:
                    return graphItemAt(item.parentItem())
                return None

            graphicItem = graphItemAt(self.itemAt(event.pos()))
            pos = self.mapToScene(event.pos())

            if graphicItem is None:

                if self.__class__._clipboardData is not None:

                    contextMenu = QtGui.QMenu(self.getGraphViewWidget())
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
                contextMenu = QtGui.QMenu(self.getGraphViewWidget())
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

