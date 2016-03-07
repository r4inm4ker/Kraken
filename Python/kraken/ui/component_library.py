
import sys
import os

import difflib

from PySide import QtGui, QtCore

from kraken.core.maths import Vec2
from kraken.core.kraken_system import KrakenSystem


class ComponentTreeWidget(QtGui.QTreeWidget):
    """Component Tree Widget"""

    def __init__(self, parent):
        super(ComponentTreeWidget, self).__init__(parent)
        self.setObjectName('ComponentTree')
        self.header().close()
        self.setColumnCount(1)
        self.setDragEnabled(True)
        self.setDragDropMode(QtGui.QTreeWidget.DragOnly)

        krakenUIWidget = self.parent().parent()
        graphViewWidget = krakenUIWidget.graphViewWidget

        krakenUIWidget.error_loading_startup = False
        if not self.generateData():
            krakenUIWidget.error_loading_startup = True
            # Wait until right after the window is displayed for the first time to call reportMessage


        self.buildWidgets()


    def buildWidgets(self):
        """Method to build the tree widgets."""

        self.clear()
        self.__iterateOnData(self._data, parentWidget=self)


    def __iterateOnData(self, data, parentWidget=None):
        """Private method to recursively build the tree widgets.

        Args:
            data (dict): Data to iterate on.

        """

        for item in data['components']:
            if data['components'][item] not in self.ks.registeredComponents.keys():
                print ("Warning: Component module "+data['components'][item]+" not found in registered components:")
                for component in self.ks.registeredComponents:
                    print "  "+component
                continue

            treeItem = QtGui.QTreeWidgetItem(parentWidget)
            treeItem.setData(0, QtCore.Qt.UserRole, data['components'][item])
            treeItem.setText(0, item)
            component = self.ks.registeredComponents[data['components'][item]]
            module = sys.modules[component.__module__]
            treeItem.setToolTip(0, module.__file__)

            if parentWidget is not None:
                parentWidget.setToolTip(0, os.path.dirname(module.__file__))

        for item in data['subDirs'].keys():

            treeItem = QtGui.QTreeWidgetItem(parentWidget)
            treeItem.setData(0, QtCore.Qt.UserRole, 'Folder')
            treeItem.setText(0, item)

            self.__iterateOnData(data['subDirs'][item], parentWidget=treeItem)


    def generateData(self):
        """Generates a dictionary with a tree structure of the component paths.

        Returns:
            True if successful

        """

        self.ks = KrakenSystem.getInstance()
        isSuccessful = self.ks.loadComponentModules()

        componentClassNames = []
        for componentClassName in sorted(self.ks.getComponentClassNames()):
            cmpCls = self.ks.getComponentClass(componentClassName)
            if cmpCls.getComponentType() != 'Guide':
                continue

            componentClassNames.append(componentClassName)


        self._data  = {'subDirs': {}, 'components': {}}

        for classItem in componentClassNames:

            nameSplit = classItem.rsplit('.', 1)

            className = nameSplit[-1]
            path = nameSplit[0].split('.')
            path.pop(len(path) - 1)

            parent = None
            for i, part in enumerate(path):

                if i == 0:
                    if part not in self._data['subDirs'].keys():
                        self._data['subDirs'][part] = {'subDirs': {}, 'components': {}}

                    parent = self._data['subDirs'][part]

                    continue

                if part in parent['subDirs'].keys():
                        parent = parent['subDirs'][part]
                        continue

                parent['subDirs'][part] = {'subDirs': {}, 'components': {}}
                parent = parent['subDirs'][part]

            parent['components'][className] = classItem

        return isSuccessful


    def mouseMoveEvent(self, event):
        self.dragObject()


    def dragObject(self):

        if not self.selectedIndexes():
            return

        item = self.selectedItems()[0]
        role = item.data(0, QtCore.Qt.UserRole)

        if role == 'Folder':
            return

        text = 'KrakenComponent:' + role

        mimeData = QtCore.QMimeData()
        mimeData.setText(text)

        drag = QtGui.QDrag(self)
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

        self.componentTreeWidget = ComponentTreeWidget(self)

        grid = QtGui.QGridLayout()
        grid.addWidget(self.componentTreeWidget, 0, 0)
        self.setLayout(grid)