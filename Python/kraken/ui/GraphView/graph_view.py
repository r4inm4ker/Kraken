#
# Copyright 2010-2015
#

import json, difflib
import os.path

from PySide import QtGui, QtCore
from graph import Graph
from node import Node, NodeTitle
from port import PortLabel, InputPort, OutputPort

from kraken.core.maths import Vec2
from kraken.core.kraken_system import KrakenSystem


class GraphView(QtGui.QGraphicsView):

    _clipboardData = None

    def __init__(self, parent=None):
        super(GraphView, self).__init__(parent)
        self.setObjectName('graphView')

        self.__graphViewWidget = parent
        self.rig = None
        self.graph = None

        self.resize(600, 400)

        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setRenderHint(QtGui.QPainter.TextAntialiasing)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.setAcceptDrops(True)

    ################################################
    ## Graph
    def init(self, rig):
        self.rig = rig
        self.graph = Graph(self, rig)
        self.setScene(self.graph.scene())

    def getGraphViewWidget(self):
        return self.__graphViewWidget

    def getGraph(self):
        return self.graph


    ################################################
    ## Graph
    def frameSelectedNodes(self):
        self.graph.frameSelectedNodes()

    def frameAllNodes(self):
        self.graph.frameAllNodes()

    def deleteSelectedNodes(self):
        self.graph.deleteSelectedNodes()


    ################################################
    ## Events
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.RightButton:

            def __getGraphItem(graphicItem):
                if isinstance(graphicItem, Node):
                    return graphicItem
                elif(isinstance(graphicItem, QtGui.QGraphicsTextItem) or
                     isinstance(graphicItem, NodeTitle) or
                     isinstance(graphicItem, OutputPort) or
                     isinstance(graphicItem, InputPort)):
                    return __getGraphItem(graphicItem.parentItem())
                return None

            pos = self.getGraph().mapToScene(event.pos())
            graphicItem = __getGraphItem(self.itemAt(int(pos.x()), int(pos.y())))

            if graphicItem is None:

                if self.__class__._clipboardData is not None:

                    contextMenu = QtGui.QMenu(self.__graphViewWidget)
                    contextMenu.setObjectName('rightClickContextMenu')
                    contextMenu.setMinimumWidth(150)

                    def pasteSettings():
                        self.graph.pasteSettings(self.__class__._clipboardData, pos)

                    contextMenu.addAction("Paste").triggered.connect(pasteSettings)
                    contextMenu.popup(event.globalPos())


            if isinstance(graphicItem, Node) and graphicItem.isSelected():
                contextMenu = QtGui.QMenu(self.__graphViewWidget)
                contextMenu.setObjectName('rightClickContextMenu')
                contextMenu.setMinimumWidth(150)

                def copySettings():
                    self.__class__._clipboardData = self.graph.copySettings(pos)

                contextMenu.addAction("Copy").triggered.connect(copySettings)

                if self.__class__._clipboardData is not None:

                    def pasteSettings():
                        # Paste the settings, not modifying the location, because that will be used to determine symmetry.
                        graphicItem.getComponent().pasteData(self.__class__._clipboardData['components'][0], setLocation=False)

                    contextMenu.addSeparator()
                    contextMenu.addAction("Paste Data").triggered.connect(pasteSettings)

                contextMenu.popup(event.globalPos())

        elif event.button() == QtCore.Qt.MouseButton.LeftButton:

            graphViewWidget = self.parent()
            contextualNodeList = graphViewWidget.getContextualNodeList()
            if contextualNodeList is not None and contextualNodeList.isVisible():
                contextualNodeList.searchLineEdit.clear()
                contextualNodeList.hide()

            else:
                super(GraphView, self).mousePressEvent(event)

        else:
            super(GraphView, self).mousePressEvent(event)

    def dragEnterEvent(self, event):
        textParts = event.mimeData().text().split(':')
        if textParts[0] == 'KrakenComponent':
            event.accept()
        else:
            event.setDropAction(QtCore.Qt.IgnoreAction)
            super(GraphView, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        super(GraphView, self).dragMoveEvent(event)
        event.accept()

    def dropEvent(self, event):
        textParts = event.mimeData().text().split(':')
        if textParts[0] == 'KrakenComponent':
            componentClassName = textParts[1]

            # Add a component to the rig placed at the given position.
            dropPosition = self.graph.mapToItem(self.graph.itemGroup(), event.pos())

            # construct
            self.graph.constructNewComponent(componentClassName, Vec2(dropPosition.x(), dropPosition.y()) );

            event.acceptProposedAction()
        else:
            super(GraphView, self).dropEvent(event)

    def resizeEvent(self, event):
        self.graph.resize(event.size())

    def closeEvent(self, event):
        return super(GraphView, self).closeEvent(event)
