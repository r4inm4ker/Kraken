

from kraken.ui.undoredo.undo_redo_manager import Command


class SelectionChangeCommand(Command):
    def __init__(self, graph, deselectedNodes, selectedNodes):
        super(SelectionChangeCommand, self).__init__()
        self.graph = graph
        self.deselectedNodes = deselectedNodes
        self.selectedNodes = selectedNodes

        self.desc = "Deselected: ["
        for i in range(len(self.deselectedNodes)):
            if i == 0:
                self.desc = self.desc + self.deselectedNodes[i].getName()
            else:
                self.desc = self.desc +", " + self.deselectedNodes[i].getName()
        self.desc = self.desc + "], Selected: ["
        for i in range(len(self.selectedNodes)):
            if i == 0:
                self.desc = self.desc + self.selectedNodes[i].getName()
            else:
                self.desc = self.desc +", " + self.selectedNodes[i].getName()
        self.desc = self.desc + "]"

    def shortDesc(self):
        return self.desc


    def redo(self):
        for node in self.selectedNodes:
            self.graph.selectNode(node, emitSignal=False)
        for node in self.deselectedNodes:
            self.graph.deselectNode(node, emitSignal=False)


    def undo(self):
        for node in self.selectedNodes:
            self.graph.deselectNode(node, emitSignal=False)
        for node in self.deselectedNodes:
            self.graph.selectNode(node, emitSignal=False)


class AddNodeCommand(Command):
    def __init__(self, graph, rig, node):
        super(AddNodeCommand, self).__init__()
        self.graph = graph
        self.rig = rig
        self.node = node


    def shortDesc(self):
        return "Add Node '" + self.node.getName() + "'"


    def redo(self):
        self.graph.addNode(self.node, emitSignal=False)
        self.node.getComponent().attach(self.rig)


    def undo(self):
        self.graph.removeNode(self.node, emitSignal=False)
        self.node.getComponent().detach()


class RemoveNodeCommand(Command):
    def __init__(self, graph, rig, node):
        super(RemoveNodeCommand, self).__init__()
        self.graph = graph
        self.rig = rig
        self.node = node


    def shortDesc(self):
        return "Add Node '" + self.node.getName() + "'"


    def redo(self):
        self.graph.removeNode(self.node, emitSignal=False)
        self.node.getComponent().detach()


    def undo(self):
        self.graph.addNode(self.node, emitSignal=False)
        self.node.getComponent().attach(self.rig)


class NodesMoveCommand(Command):
    def __init__(self, graph, nodes, delta):
        super(NodesMoveCommand, self).__init__()
        self.graph = graph
        self.nodes = nodes
        self.delta = delta
        self.desc = "Moved: "
        for node in self.nodes:
            self.desc = self.desc +", " + node.getName()


    def shortDesc(self):
        return self.desc


    def redo(self):
        for node in self.nodes:
            node.translate( self.delta.x(), self.delta.y())


    def undo(self):
        for node in self.nodes:
            node.translate( -self.delta.x(), -self.delta.y())



class ConnectionAddedCommand(Command):
    def __init__(self, graph, rig, connection):
        super(ConnectionAddedCommand, self).__init__()
        self.graph = graph
        self.connection = connection

        self.sourceComponent = rig.getChildByDecoratedName(self.connection.getSrcPort().getNode().getName())
        self.targetComponent = rig.getChildByDecoratedName(self.connection.getDstPort().getNode().getName())

        self.sourceComponentOutputPort = self.sourceComponent.getOutputByName(self.connection.getSrcPort().getName())
        self.targetComponentInputPort = self.targetComponent.getInputByName(self.connection.getDstPort().getName())

        self.targetComponentInputPort.setConnection(self.sourceComponentOutputPort)

    def shortDesc(self):
        return "Connect Ports '" + self.connection.getSrcPort().getName() + " > " + self.connection.getDstPort().getName()


    def redo(self):
        self.targetComponentInputPort.setConnection(self.sourceComponentOutputPort)
        self.connection.connect()
        self.graph.addConnection(self.connection, emitSignal=False)


    def undo(self):
        self.targetComponentInputPort.removeConnection()
        self.graph.removeConnection(self.connection, emitSignal=False)


class ConnectionRemovedCommand(Command):
    def __init__(self, graph, rig, connection):
        super(ConnectionRemovedCommand, self).__init__()
        self.graph = graph
        self.connection = connection

        self.sourceComponent = rig.getChildByDecoratedName(self.connection.getSrcPort().getNode().getName())
        self.targetComponent = rig.getChildByDecoratedName(self.connection.getDstPort().getNode().getName())

        self.sourceComponentOutputPort = self.sourceComponent.getOutputByName(self.connection.getSrcPort().getName())
        self.targetComponentInputPort = self.targetComponent.getInputByName(self.connection.getDstPort().getName())

        self.targetComponentInputPort.removeConnection()

    def shortDesc(self):
        return "Disconnect Ports '" + self.connection.getSrcPort().getName() + " > " + self.connection.getDstPort().getName()


    def redo(self):
        self.targetComponentInputPort.removeConnection()
        self.graph.removeConnection(self.connection, emitSignal=False)

    def undo(self):
        self.targetComponentInputPort.setConnection(self.sourceComponentOutputPort)
        self.connection.connect()
        self.graph.addConnection(self.connection, emitSignal=False)

