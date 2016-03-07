#
# Copyright 2010-2015
#

import difflib

from PySide import QtGui, QtCore

from kraken.core.maths import Vec2
from kraken.core.kraken_system import KrakenSystem
from knode import KNode


class NodeList(QtGui.QListWidget):

    def __init__(self, parent):
        # constructors of base classes
        QtGui.QListWidget.__init__(self, parent)
        self.setObjectName('contextNodeList')
        self.installEventFilter(self)


    def eventFilter(self, object, event):
        if event.type()== QtCore.QEvent.WindowDeactivate:
            self.parent().close()
            return True
        elif event.type()== QtCore.QEvent.FocusOut:
            self.parent().close()
            return True

        return False


class SearchLineEdit(QtGui.QLineEdit):

    def __init__(self, parent):
        super(SearchLineEdit, self).__init__(parent)

    def focusOutEvent(self, event):
        self.parent().close()


class ContextualNodeList(QtGui.QWidget):

    def __init__(self, parent):
        super(ContextualNodeList, self).__init__(parent)

        self.setFixedSize(250, 200)

        self.searchLineEdit = SearchLineEdit(self)
        self.searchLineEdit.setObjectName('contextNodeListSearchLine')
        # self.searchLineEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.searchLineEdit.setFocus()

        self.nodesList = NodeList(self)

        self.ks = KrakenSystem.getInstance()

        self.componentClassNames = []
        for componentClassName in sorted(self.ks.getComponentClassNames()):
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


    def showAtPos(self, pos, graphpos, graph):
        self.graph = graph
        posx = pos.x() - self.width() * 0.1
        self.move(posx, pos.y() - 20)
        self.pos = pos
        self.graphpos = graphpos
        self.searchLineEdit.setFocus()
        self.searchLineEdit.clear()
        self.showClosestNames()
        self.show()

    def createNode(self):
        if self.nodesList.currentItem() is not None:

            componentClassName = self.nodesList.currentItem().data(QtCore.Qt.UserRole)

            componentClass = self.ks.getComponentClass(componentClassName)
            component = componentClass(parent=self.graph.getRig())
            component.setGraphPos(Vec2(self.graphpos.x(), self.graphpos.y()))
            node = KNode(self.graph, component)
            self.graph.addNode(node)
            self.graph.selectNode(node, clearSelection=True, emitSignal=False)

            if self.isVisible():
                self.close()

    def showClosestNames(self):

        self.nodesList.clear()
        fuzzyText = self.searchLineEdit.text()

        for componentClassName in self.componentClassNames:
            shortName = componentClassName.rsplit('.', 1)[-1]

            if fuzzyText != '':
                if fuzzyText.lower() not in shortName.lower():
                    continue

            item = QtGui.QListWidgetItem(shortName)
            item.setData(QtCore.Qt.UserRole, componentClassName)
            self.nodesList.addItem(item)

        self.nodesList.resize(self.nodesList.frameSize().width(), 20 * self.nodesList.count())

        self.setIndex(0)

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
                self.close()

        elif event.key() == QtCore.Qt.Key_Up or event.key() == QtCore.Qt.Key_Down:
            if event.key() == QtCore.Qt.Key_Up:
                newIndex = self.index - 1
                if newIndex not in range(self.nodesList.count()):
                    return

                self.setIndex(self.index-1)
            elif event.key() == QtCore.Qt.Key_Down:
                newIndex = self.index+1
                if newIndex not in range(self.nodesList.count()):
                    return

                self.setIndex(self.index+1)

        elif event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
            if self.isVisible():
                self.createNode()
                self.close()

        return False

    def focusOutEvent(self, event):
        self.close()