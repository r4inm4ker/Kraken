#
# Copyright 2010-2015
#

import difflib

from PySide import QtGui, QtCore

from kraken.core.maths import Vec2
from kraken.core.kraken_system import KrakenSystem


class NodeList(QtGui.QListWidget):

    def __init__(self, parent):
        # constructors of base classes
        QtGui.QListWidget.__init__(self, parent)
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

    def __init__(self, parent, graph):
        super(ContextualNodeList, self).__init__(parent)

        self.graph = graph
        self.setFixedSize(250, 200)

        self.searchLineEdit = QtGui.QLineEdit(parent)
        self.searchLineEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.searchLineEdit.setFocus()

        self.nodesList = NodeList(self)

        self.ks = KrakenSystem.getInstance()
        self.ks.loadIniFile()

        self.componentClassNames = []
        for componentClassName in self.ks.getComponentClassNames():
            cmpCls = self.ks.getComponentClass(componentClassName)
            if cmpCls.getComponentType() != 'Guide':
                continue

            self.componentClassNames.append(componentClassName)

        self.nodes = None
        self.showClosestNames()
        self.searchLineEdit.textEdited.connect(self.showClosestNames)
        self.nodesList.itemClicked.connect(self.createNode)

        self.setIndex(0)

        grid = QtGui.QGridLayout()
        grid.addWidget(self.searchLineEdit, 0, 0)
        grid.addWidget(self.nodesList, 1, 0)
        self.setLayout(grid)


    def showAtPos(self, pos, graphpos):
        posx = pos.x() - self.width() * 0.1
        self.move(posx, pos.y() - 20)
        self.pos = pos
        self.graphpos = graphpos
        self.searchLineEdit.setFocus()
        self.searchLineEdit.clear()
        self.show()


    def createNode(self):
        if self.nodesList.currentItem() is not None:

            componentClassName = self.nodesList.currentItem()._fullClassName

            # Add a component to the rig placed at the given position.
            dropPosition = self.graph.mapToItem(self.graph.itemGroup(), self.pos)

            # Construct the component.
            krakenSystem = KrakenSystem.getInstance()
            componentClass = krakenSystem.getComponentClass(componentClassName)
            component = componentClass(parent=self.graph.getRig())
            component.setGraphPos(Vec2(dropPosition.x(), dropPosition.y()))

            self.graph.addNode(component)

            if self.isVisible():
                self.hide()

    def showClosestNames(self):

        self.nodesList.clear()
        fuzzyText = self.searchLineEdit.text()
        matches = difflib.get_close_matches(fuzzyText, [x.rsplit('.', 1)[-1] for x in self.componentClassNames], n=3, cutoff=0.2)

        for componentClassName in self.componentClassNames:
            shortName = componentClassName.rsplit('.', 1)[-1]

            if fuzzyText != '':
                if fuzzyText.lower() not in shortName.lower():
                    continue

            # if fuzzyText != '' and shortName not in matches:
            #     continue

            cmpCls = self.ks.getComponentClass(componentClassName)
            if cmpCls.getComponentType() != 'Guide':
                continue

            item = QtGui.QListWidgetItem(shortName)
            item._fullClassName = componentClassName
            self.nodesList.addItem(item)

        self.nodesList.resize(self.nodesList.frameSize().width(), 20 * self.nodesList.count())


    def setIndex(self, index):

        if index > len(self.componentClassNames):
            return

        if index >= 0:
            self.index = index
            self.nodesList.setCurrentItem(self.nodesList.item(self.index))


    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            if self.isVisible():
                self.searchLineEdit.clear()
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

    def __init__(self, parent, graph, objectType, pos):
        super(ContextualNewNodeWidget, self).__init__(parent)

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

        # if self.objectType == 'graph':
        #     nodes = self.graph.getSelectedNodes()
        #     names = ""
        #     nodePaths = []
        #     for node in nodes:
        #         names += (" " + node.getName())
        #         nodePaths.append(node.getNodePath())
        #     self.controller.beginInteraction("Create Graph from nodes:"+ str(names));
        #     self.graph.clearSelection()
        #     newGraphPath = self.controller.newGraphNode(
        #         executablePath=executablePath,
        #         graphPath=self.graph.getGraphPath(),
        #         graphPos=QtCore.QPointF(self.pos.x() - 40, self.pos.y() + 20),
        #         nodePaths=nodePaths
        #     )
        # elif self.objectType == 'function':

        #     self.controller.beginInteraction("Create Node");
        #     # Note: newFunctionNode might midfy the path by inserting 'Fabric' at the begining (Hack to be removed ASAP)
        #     executablePath = self.controller.newFunctionNode(
        #         executablePath=executablePath
        #     )

        #     # Add a node to the graph at the given position.
        #     self.controller.addNode(
        #         graphPath=self.graph.getGraphPath(),
        #         executablePath=executablePath,
        #         graphPos=QtCore.QPointF(self.pos.x() - 40, self.pos.y() + 20)
        #     )

        # self.controller.endInteraction()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            if self.isVisible():
                self.close()

        if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
            if self.isVisible():
                self.createNode()
                self.close()
            return True
