

#
# Copyright 2010-2015
#

from PySide import QtGui, QtCore

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

class ContextualNodeList(QtGui.QWidget):


    def __init__(self, parent, controller, graph):
        super(ContextualNodeList, self).__init__(parent)

        self.controller = controller
        self.graph = graph
        self.setFixedSize(250, 200)

        self.searchLineEdit = QtGui.QLineEdit(parent)
        self.searchLineEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.searchLineEdit.setFocus()

        self.nodesList = NodeList(self, controller)

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
