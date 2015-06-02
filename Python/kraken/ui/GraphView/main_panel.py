
#
# Copyright 2010-2015
#

from PySide import QtGui, QtCore
from selection_rect import SelectionRect


class MainPanel(QtGui.QGraphicsWidget):
    __backgroundColor = QtGui.QColor(50, 50, 50)
    __gridPenS = QtGui.QPen(QtGui.QColor(44, 44, 44, 255), 0.5)
    __gridPenL = QtGui.QPen(QtGui.QColor(40, 40, 40, 255), 1.0)
    __gridPenA = QtGui.QPen(QtGui.QColor(30, 30, 30, 255), 2.0)

    __mouseWheelZoomRate = 0.001

    def __init__(self, graph):
        super(MainPanel, self).__init__(graph)

        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))
        self.setAcceptDrops(True)

        self.graph = graph
        self.__itemGroup = QtGui.QGraphicsWidget(self)

        self._manipulationMode = 0
        self._dragging = False
        self._selectionRect = None

    def itemGroup(self):
        return self.__itemGroup

    def mousePressEvent(self, event):
        if event.button() is QtCore.Qt.MouseButton.LeftButton:
            mouseDownPos = self.mapToItem(self.graph.itemGroup(), event.pos())
            self._selectionRect = SelectionRect(self.__itemGroup, mouseDownPos)
            self._dragging = False
            self._manipulationMode = 1
        elif event.button() is QtCore.Qt.MouseButton.MiddleButton:
            self.setCursor(QtCore.Qt.OpenHandCursor)
            self._manipulationMode = 2
            self._lastPanPoint = event.pos()
        else:
            super(MainPanel, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._manipulationMode == 1:
            dragPoint = self.mapToItem(self.graph.itemGroup(), event.pos())
            self._selectionRect.setDragPoint(dragPoint)
            self.graph.clearSelection()
            for name, node in self.graph.getNodes().iteritems():
                if not node.isSelected() and self._selectionRect.collidesWithItem(node):
                    self.graph.selectNode(node)
            self._dragging = True

        elif self._manipulationMode == 2:
            (xfo, invRes) = self.__itemGroup.transform().inverted()
            delta = xfo.map(event.pos()) - xfo.map(self._lastPanPoint)
            self._lastPanPoint = event.pos()
            self.__itemGroup.translate(delta.x(), delta.y())
        else:
            super(MainPanel, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self._manipulationMode == 1:
            self.scene().removeItem(self._selectionRect)
            if not self._dragging:
                self.graph.clearSelection()
            self._selectionRect = None
            self._manipulationMode = 0
        elif self._manipulationMode == 2:
            self.setCursor(QtCore.Qt.ArrowCursor)
            self._manipulationMode = 0
        else:
            super(MainPanel, self).mouseReleaseEvent(event)

    def wheelEvent(self, event):

        (xfo, invRes) = self.__itemGroup.transform().inverted()
        topLeft = xfo.map(self.rect().topLeft())
        bottomRight = xfo.map(self.rect().bottomRight())
        center = ( topLeft + bottomRight ) * 0.5

        zoomFactor = 1.0 + event.delta() * self.__mouseWheelZoomRate
        transform = self.__itemGroup.transform()
        transform.scale(zoomFactor, zoomFactor)

        if transform.m22() > 0.01: # To avoid negative scalling as it would flip the graph
            self.__itemGroup.setTransform(transform)

            (xfo, invRes) = transform.inverted()
            topLeft = xfo.map(self.rect().topLeft())
            bottomRight = xfo.map(self.rect().bottomRight())
            newcenter = ( topLeft + bottomRight ) * 0.5

            # Re-center the graph on the old position.
            self.__itemGroup.translate(newcenter.x() - center.x(), newcenter.y() - center.y())

    def paint(self, painter, option, widget):
        # return super(MainPanel, self).paint(painter, option, widget)

        rect = self.__itemGroup.mapRectFromParent(self.windowFrameRect())

        oldTransform = painter.transform()
        painter.setTransform(self.__itemGroup.transform(), True)

        painter.fillRect(rect, self.__backgroundColor)

        gridSize = 30
        left = int(rect.left()) - (int(rect.left()) % gridSize)
        top = int(rect.top()) - (int(rect.top()) % gridSize)

        # Draw horizontal fine lines
        gridLines = []
        painter.setPen(self.__gridPenS)
        y = float(top)
        while y < float(rect.bottom()):
            gridLines.append(QtCore.QLineF( rect.left(), y, rect.right(), y ))
            y += gridSize
        painter.drawLines(gridLines)

        # Draw vertical fine lines
        gridLines = []
        painter.setPen(self.__gridPenS)
        x = float(left)
        while x < float(rect.right()):
            gridLines.append(QtCore.QLineF( x, rect.top(), x, rect.bottom()))
            x += gridSize
        painter.drawLines(gridLines)

        # Draw thick grid
        gridSize = 30 * 10
        left = int(rect.left()) - (int(rect.left()) % gridSize)
        top = int(rect.top()) - (int(rect.top()) % gridSize)

        # Draw vertical thick lines
        gridLines = []
        painter.setPen(self.__gridPenL)
        x = left
        while x < rect.right():
            gridLines.append(QtCore.QLineF( x, rect.top(), x, rect.bottom() ))
            x += gridSize
        painter.drawLines(gridLines)

        # Draw horizontal thick lines
        gridLines = []
        painter.setPen(self.__gridPenL)
        y = top
        while y < rect.bottom():
            gridLines.append(QtCore.QLineF( rect.left(), y, rect.right(), y ))
            y += gridSize
        painter.drawLines(gridLines)

        painter.setTransform(oldTransform)

        return super(MainPanel, self).paint(painter, option, widget)

