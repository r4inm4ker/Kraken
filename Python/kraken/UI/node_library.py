
#
# Copyright 2010-2015
#
import sys
import json
from PySide import QtGui, QtCore
from kraken.core.kraken_system import KrakenSystem

import kraken.examples.spine_component
import kraken.examples.arm_component
import kraken.examples.leg_component

class NodeLibrary(QtGui.QWidget):

    class NodeTree(QtGui.QTreeWidget):

        def __init__(self, parent=None):
            # constructors of base classes
            QtGui.QTreeWidget.__init__(self, parent)

            self.setDragEnabled(True)
            self.setDragDropMode(QtGui.QTreeWidget.DragOnly)
            self.setColumnCount(1)
            self.setHeaderLabels([''])

        def mouseMoveEvent(self, event):
            self.dragObject()

        def dragObject(self):
            if not self.selectedIndexes():
                return
            drag = QtGui.QDrag(self)
            text = 'KrakenComponent:' + self.selectedItems()[0].text(0)

            mimeData = QtCore.QMimeData()
            mimeData.setText(text)

            drag.setMimeData(mimeData)
            drag.setHotSpot(QtCore.QPoint(90, 23))

            ghostNode = QtGui.QPixmap(180, 46)
            ghostNode.fill(QtGui.QColor(200, 200, 200, 80))

            drag.setPixmap(ghostNode)
            drag.start(QtCore.Qt.IgnoreAction)


    def __init__(self, parent=None):
        super(NodeLibrary, self).__init__(parent)

        self.ks = KrakenSystem.getInstance()
        self.ks.loadIniFile()
        # self.controller = controller
        self.searchLineEdit = QtGui.QLineEdit(self)
        self.searchLineEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.searchLineEdit.setFocus()

        self.nodesList = NodeLibrary.NodeTree(parent)

        grid = QtGui.QGridLayout(self)
        grid.addWidget(self.searchLineEdit, 0, 0)
        grid.addWidget(self.nodesList, 1, 0)

        self.componentNames = self.ks.getComponentClassNames()

        self.showClosestNames()
        self.searchLineEdit.textEdited.connect(self.showClosestNames)

    def showClosestNames(self):
        self.nodesList.clear()
        fuzzyText = self.searchLineEdit.text()

        for cmpName in self.componentNames:
            add = True
            if fuzzyText != '':
                if fuzzyText.lower() not in cmpName.lower():
                    add = False
            if add:
                treeItem = QtGui.QTreeWidgetItem()
                treeItem.setText(0, cmpName)
                # treeItem.setData(0, QtCore.Qt.UserRole, path)
                self.nodesList.addTopLevelItem(treeItem)

        self.nodesList.expandAll()




if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    widget = NodeLibrary()
    widget.show()
    sys.exit(app.exec_())

