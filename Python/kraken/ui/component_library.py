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
        self.setObjectName('ComponentTree')

        self.setDragEnabled(True)
        self.setDragDropMode(QtGui.QTreeWidget.DragOnly)

    def mouseMoveEvent(self, event):
        self.dragObject()

    def dragObject(self):

        if not self.selectedIndexes():
            return

        drag = QtGui.QDrag(self)
        item = self.selectedItems()[0]
        componentClassName = item.data(QtCore.Qt.UserRole)
        text = 'KrakenComponent:' + componentClassName

        mimeData = QtCore.QMimeData()
        mimeData.setText(text)

        drag.setMimeData(mimeData)
        drag.setHotSpot(QtCore.QPoint(90, 23))

        ghostComponent = QtGui.QPixmap(180, 46)
        ghostComponent.fill(QtGui.QColor(67, 143, 153, 80))

        drag.setPixmap(ghostComponent)
        drag.start(QtCore.Qt.IgnoreAction)


class ComponentLibrary(QtGui.QWidget):

    def __init__(self, parent):
        super(ComponentLibrary, self).__init__(parent)

        self.setMinimumWidth(175)

        self.searchLineEdit = QtGui.QLineEdit(parent)
        self.searchLineEdit.setObjectName('contextNodeListSearchLine')
        # self.searchLineEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        # self.searchLineEdit.setFocus()

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

        self.setIndex(0)

        grid = QtGui.QGridLayout()
        grid.addWidget(self.searchLineEdit, 0, 0)
        grid.addWidget(self.nodesList, 1, 0)
        self.setLayout(grid)


    def showClosestNames(self):

        self.nodesList.clear()
        fuzzyText = self.searchLineEdit.text()

        for componentClassName in self.componentClassNames:
            shortName = componentClassName.rsplit('.', 1)[-1]

            if fuzzyText != '':
                if fuzzyText.lower() not in shortName.lower():
                    continue

            cmpCls = self.ks.getComponentClass(componentClassName)
            if cmpCls.getComponentType() != 'Guide':
                continue

            item = QtGui.QListWidgetItem(shortName)
            item._fullClassName = componentClassName
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

        modifiers = event.modifiers()
        if event.key() == QtCore.Qt.Key_Escape:
            if self.isVisible():
                self.searchLineEdit.clear()
                self.hide()

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
                self.hide()

        # Ctrl+W
        elif event.key() == 87 and modifiers == QtCore.Qt.ControlModifier:
            self.window().close()

        return False
