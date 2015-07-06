

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
        self.node = self.graph.addNode(self.component)

    def undo(self):
        self.graph.removeNode(self.node)


