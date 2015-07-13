

from kraken.core.kraken_system import KrakenSystem
from kraken.ui.undoredo.undo_redo_manager import UndoRedoManager, Command

class SelectNodeCommand(Command):
    def __init__(self, graph, node, clearSelection=False):
        super(SelectNodeCommand, self).__init__()
        self.graph = graph
        self.node = node
        self.clearSelection = clearSelection

    def shortDesc(self):
        return "Select Node '" + self.node.getName() + "'"


    def redo(self):
        self.graph.selectNode(self.node, clearSelection=self.clearSelection)


    def undo(self):
        self.graph.deselectNode(self.node)

class DeselectNodeCommand(Command):
    def __init__(self, graph, node):
        super(DeselectNodeCommand, self).__init__()
        self.graph = graph
        self.node = node


    def shortDesc(self):
        return "Deselect Node '" + self.node.getName() + "'"


    def redo(self):
        self.graph.deselectNode(self.node)


    def undo(self):
        self.graph.selectNode(self.node, clearSelection=False)



class SelectionChangeCommand(Command):
    def __init__(self, graph, selectedNodes, deselectedNodes):
        super(SelectionChangeCommand, self).__init__()
        self.graph = graph
        self.selectedNodes = selectedNodes
        self.deselectedNodes = deselectedNodes

        self.desc = "Deselected: "
        for node in self.deselectedNodes:
            self.desc = self.desc +", " + node.getName();
        self.desc = self.desc + "Selected: "
        for node in self.selectedNodes:
            self.desc = self.desc +", " + node.getName();

    def shortDesc(self):
        return self.desc


    def redo(self):
        for node in self.selectedNodes:
            self.graph.selectNode(node)
        for node in self.deselectedNodes:
            self.graph.deselectNode(node)


    def undo(self):
        for node in self.selectedNodes:
            self.graph.deselectNode(node)
        for node in self.deselectedNodes:
            self.graph.selectNode(node)

        

class NodeMoveCommand(Command):
    def __init__(self, nodes, delta):
        super(NodeMoveCommand, self).__init__()
        self.nodes = nodes
        self.delta = delta
        self.desc = "Moved: "
        for node in self.nodes:
            self.desc = self.desc +", " + node.getName();


    def shortDesc(self):
        return self.desc


    def redo(self):
        for node in self.nodes:
            node.translate( self.delta.x(), self.delta.y())
            node.pushGraphPosToComponent()


    def undo(self):
        for node in self.nodes:
            node.translate( -self.delta.x(), -self.delta.y())
            node.pushGraphPosToComponent()
        

class AddNodeCommand(Command):
    def __init__(self, graph, rig, node):
        super(AddNodeCommand, self).__init__()
        self.graph = graph
        self.rig = rig
        self.node = node
        self.destoryNode = False


    def shortDesc(self):
        return "Add Node '" + self.node.getName() + "'"


    def redo(self):
        self.graph.addNode(self.node, emitNotification=False)
        self.rig.addChild( self.node.getComponent() )
        self.destoryNode = False


    def undo(self):
        self.graph.removeNode(self.node, destroy=False, emitNotification=False)
        self.rig.removeChild( self.node.getComponent() )
        self.destoryNode = True


    def destroy(self):
        if self.destoryNode:
            self.node.destroy()


class RemoveNodeCommand(Command):
    def __init__(self, graph, rig, node):
        super(RemoveNodeCommand, self).__init__()
        self.graph = graph
        self.rig = rig
        self.node = node
        self.destoryNode = False


    def shortDesc(self):
        return "Add Node '" + self.node.getName() + "'"


    def redo(self):
        self.graph.removeNode(self.node, destroy=False, emitNotification=False)
        self.rig.removeChild( self.node.getComponent() )
        self.destoryNode = True


    def undo(self):
        self.graph.addNode(self.node, emitNotification=False)
        self.rig.addChild( self.node.getComponent() )
        self.destoryNode = False


    def destroy(self):
        if self.destoryNode:
            self.node.destroy()


class ConstructComponentCommand(Command):
    def __init__(self, graph, componentClassName, graphPos):
        super(ConstructComponentCommand, self).__init__()
        self.graph = graph
        self.componentClassName = componentClassName
        self.graphPos = graphPos
        krakenSystem = KrakenSystem.getInstance()
        self.componentClass = krakenSystem.getComponentClass( componentClassName )


    def shortDesc(self):
        return "Add Component '" + self.componentClassName + "'"


    def redo(self):
        self.component = self.componentClass(parent=self.graph.getRig())
        self.component.setGraphPos(self.graphPos)
        from node import Node
        self.node = self.graph.addNode(Node(self.graph, self.component) )


    def undo(self):
        self.graph.removeNode(self.node)



class PortConnectCommand(Command):
    def __init__(self, sourcePort, targetPort, graph):
        super(PortConnectCommand, self).__init__()
        self.sourcePort = sourcePort
        self.targetPort = targetPort
        self.graph = graph
        self.scene = self.graph.scene()

        self.sourceComponent = self.sourcePort.getNode().getComponent()
        self.targetComponent = self.targetPort.getNode().getComponent()

        self.sourceComponentOutputPort = self.sourceComponent.getOutputByName(self.sourcePort.getName())
        self.targetComponentInputPort = self.targetComponent.getInputByName(self.targetPort.getName())
        self.connection = None


    def shortDesc(self):
        return "Connect Ports '" + self.sourcePort.getName() + " > " + self.targetPort.getName()


    def redo(self):
        self.targetComponentInputPort.setConnection(self.sourceComponentOutputPort)
        if self.connection is None:
            self.connection = self.graph.addConnection(
                source=self.sourceComponent.getDecoratedName() + '.' + self.sourceComponentOutputPort.getName(),
                target=self.targetComponent.getDecoratedName() + '.' + self.targetComponentInputPort.getName()
            )
        else:
            self.connection.setVisible(True)


    def undo(self):
        self.targetComponentInputPort.removeConnection()
        self.connection.setVisible(False)


    def destroy(self):
        self.scene.removeItem(self.connection)


class PortDisconnectCommand(Command):
    def __init__(self, connection, graph):
        super(PortDisconnectCommand, self).__init__()
        self.connection = connection
        self.graph = graph
        self.scene = self.graph.scene()

        self.sourceComponent = self.connection.getSrcPort().getNode().getComponent()
        self.targetComponent = self.connection.getDstPort().getNode().getComponent()

        self.sourceComponentOutputPort = self.sourceComponent.getOutputByName(self.connection.getSrcPort().getName())
        self.targetComponentInputPort = self.targetComponent.getInputByName(self.connection.getDstPort().getName())


    def shortDesc(self):
        return "Disconnect Ports '" + self.connection.getSrcPort().getName() + " > " + self.connection.getDstPort().getName()


    def redo(self):
        self.targetComponentInputPort.removeConnection()
        self.connection.setVisible(False)


    def undo(self):
        self.targetComponentInputPort.setConnection(self.sourceComponentOutputPort)
        self.connection.setVisible(True)


    def destroy(self):
        self.scene.removeItem(self.connection)