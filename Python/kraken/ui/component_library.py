
#
# Copyright 2010-2015
#
import sys
import json
from PySide import QtGui, QtCore
from kraken.core.kraken_system import KrakenSystem

class _ComponentTree(QtGui.QTreeWidget):

    def __init__(self, parent=None):
        # constructors of base classes
        QtGui.QTreeWidget.__init__(self, parent)
        self.setObjectName('ComponentTree')

        self.setDragEnabled(True)
        self.setDragDropMode(QtGui.QTreeWidget.DragOnly)
        self.setColumnCount(1)
        self.setHeaderLabels([''])
        self.header().close()


    def mouseMoveEvent(self, event):
        self.dragObject()


    def dragObject(self):

        if not self.selectedIndexes():
            return

        drag = QtGui.QDrag(self)
        item = self.selectedItems()[0]
        componentClassName = item.data(0, QtCore.Qt.UserRole)
        text = 'KrakenComponent:' + componentClassName

        mimeData = QtCore.QMimeData()
        mimeData.setText(text)

        drag.setMimeData(mimeData)
        drag.setHotSpot(QtCore.QPoint(90, 23))

        ghostComponent = QtGui.QPixmap(180, 46)
        ghostComponent.fill(QtGui.QColor(200, 200, 200, 80))

        drag.setPixmap(ghostComponent)
        drag.start(QtCore.Qt.IgnoreAction)


class ComponentLibrary(QtGui.QWidget):

    def __init__(self, parent=None):
        super(ComponentLibrary, self).__init__(parent)
        self.setObjectName('ComponentLibrary')

        self.ks = KrakenSystem.getInstance()
        self.ks.loadIniFile()
        # self.controller = controller
        self.searchLineEdit = QtGui.QLineEdit(self)
        # self.searchLineEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        # self.searchLineEdit.setFocus()

        self.nodesList = _ComponentTree(parent)

        grid = QtGui.QGridLayout(self)
        grid.addWidget(self.searchLineEdit, 0, 0)
        grid.addWidget(self.nodesList, 1, 0)

        self.componentClassNames = self.ks.getComponentClassNames()

        self.showClosestNames()
        self.searchLineEdit.textEdited.connect(self.showClosestNames)


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

            treeItem = QtGui.QTreeWidgetItem()
            treeItem.setText(0, shortName)
            treeItem.setData(0, QtCore.Qt.UserRole, componentClassName)
            self.nodesList.addTopLevelItem(treeItem)

        self.nodesList.expandAll()

        self.nodesList.setCurrentItem(self.nodesList.topLevelItem(0))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    widget = ComponentLibrary()
    widget.show()
    sys.exit(app.exec_())
