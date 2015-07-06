
#
# Copyright 2010-2015
#

#pylint: disable-msg=W0613
import json
from PySide import QtGui, QtCore
from port import InputPort, OutputPort
from kraken.core.maths import Vec2

from kraken.ui.component_inspector import ComponentInspector
from kraken.ui.undoredo.undo_redo_manager import UndoRedoManager

from graph_commands import SelectNodeCommand

class NodeTitle(QtGui.QGraphicsWidget):
    __color = QtGui.QColor(25, 25, 25)
    __font = QtGui.QFont('Decorative', 14)
    __font.setLetterSpacing(QtGui.QFont.PercentageSpacing, 115)
    __labelBottomSpacing = 12

    def __init__(self, text, parent=None):
        super(NodeTitle, self).__init__(parent)

        self.__textItem = QtGui.QGraphicsTextItem(text, self)
        self.__textItem.setDefaultTextColor(self.__color)
        self.__textItem.setFont(self.__font)
        self.__textItem.setPos(0, -2)
        option = self.__textItem.document().defaultTextOption()
        option.setWrapMode(QtGui.QTextOption.NoWrap)
        self.__textItem.document().setDefaultTextOption(option)
        self.__textItem.adjustSize()

        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed))
        self.setPreferredSize(self.textSize())

    def setText(self, text):
        self.__textItem.setPlainText(text)
        self.__textItem.adjustSize()
        self.setPreferredSize(self.textSize())

    def textSize(self):
        return QtCore.QSizeF(
            self.__textItem.textWidth(),
            self.__font.pointSizeF() + self.__labelBottomSpacing
            )

    def paint(self, painter, option, widget):
        super(NodeTitle, self).paint(painter, option, widget)
        # painter.setPen(QtGui.QPen(QtGui.QColor(0, 255, 0)))
        # painter.drawRect(self.windowFrameRect())


class Node(QtGui.QGraphicsWidget):
    __defaultColor = QtGui.QColor(154, 205, 50, 255)
    __unselectedPen =  QtGui.QPen(QtGui.QColor(25, 25, 25), 1.6)
    __selectedPen =  QtGui.QPen(QtGui.QColor(255, 255, 255, 255), 1.6)
    __linePen =  QtGui.QPen(QtGui.QColor(25, 25, 25, 255), 1.25)

    def __init__(self, graph, component):
        super(Node, self).__init__(graph.itemGroup())

        self.setMinimumWidth(60)
        self.setMinimumHeight(20)
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))

        layout = QtGui.QGraphicsLinearLayout()
        layout.setContentsMargins(5, 0, 5, 7)
        layout.setSpacing(7)
        layout.setOrientation(QtCore.Qt.Vertical)
        self.setLayout(layout)

        # We have the following sources of information to display a node.
        # 1. The executable. This defines the ports of the node, and its metadata contains the color and other settings.
        # 2. The 'Node' or instance of the executable. Its meta data contains the positioin of the node in the graph.
        # 3. The 'evalDesc' (for lack of a better name). This contains the data types that have been propagated to the ports.
        # Given the graph path, and the node name, I should be able to acess the node.

        self.__graph = graph
        self.__component = component
        self.__color = QtGui.QColor(154, 205, 50, 255)
        self.__inspectorWidget = None

        self.__titleItem = NodeTitle(self.__component.getDecoratedName(), self)
        layout.addItem(self.__titleItem)
        layout.setAlignment(self.__titleItem, QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)

        self.__inports = []
        self.__outports = []
        for i in range(self.__component.getNumInputs()):
            componentInput = component.getInputByIndex(i)
            self.addInputPort(componentInput)

        # Insert space between input and output ports
        spacingWidget = QtGui.QGraphicsWidget(self)
        spacingWidget.setPreferredSize(2.0, 2.0)
        layout.addItem(spacingWidget)

        for i in range(self.__component.getNumOutputs()):
            componentOutput = component.getOutputByIndex(i)
            self.addOutputPort(componentOutput)


        self.__selected = False
        self.__dragging = False
        # self.__graph.controller().addNotificationListener('node.posChanged', self.__nodePosChanged)
        # self.__graph.controller().addNotificationListener('port.created', self.__portAdded)
        # self.__graph.controller().addNotificationListener('port.destroyed', self.__portRemoved)

        # Update the node so that the size is computed.
        self.adjustSize()

        self.setGraphPos( QtCore.QPointF( self.__component.getGraphPos().x, self.__component.getGraphPos().y ) )

    def getName(self):
        return self.__component.getDecoratedName()

    def getComponent(self):
        return self.__component

    def getGraph(self):
        return self.__graph

    #########################
    ## Ports

    def addInputPort(self, componentInput):
        port = InputPort(self, self.__graph, componentInput)

        layout = self.layout()
        layout.addItem(port)
        layout.setAlignment(port, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.__inports.append(port)
        self.adjustSize()
        return port

    def addOutputPort(self, componentOutput):
        port = OutputPort(self, self.__graph, componentOutput)

        layout = self.layout()
        layout.addItem(port)
        layout.setAlignment(port, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.__outports.append(port)
        self.adjustSize()
        return port

    def getInPort(self, name):
        for port in self.__inports:
            if port.getName() == name:
                return port
        return None

    def getOutPort(self, name):
        for port in self.__outports:
            if port.getName() == name:
                return port
        return None

    def paint(self, painter, option, widget):
        rect = self.windowFrameRect()
        painter.setBrush(self.__color)

        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0), 0))

        roundingY = 10
        roundingX = rect.height() / rect.width() * roundingY

        painter.drawRoundRect(rect, roundingX, roundingY)

        # Title BG
        titleHeight = self.__titleItem.size().height() - 3

        painter.setBrush(self.__color.darker(125))
        roundingY = rect.width() * roundingX / titleHeight
        painter.drawRoundRect(0, 0, rect.width(), titleHeight, roundingX, roundingY)
        painter.drawRect(0, titleHeight * 0.5 + 2, rect.width(), titleHeight * 0.5)

        # painter.setPen(self.__linePen)
        # painter.drawLine(QtCore.QPoint(0, titleHeight), QtCore.QPoint(rect.width(), titleHeight))

        painter.setBrush(QtGui.QColor(0, 0, 0, 0))
        if self.__selected:
            painter.setPen(self.__selectedPen)
        else:
            painter.setPen(self.__unselectedPen)

        roundingY = 10
        roundingX = rect.height() / rect.width() * roundingY

        painter.drawRoundRect(rect, roundingX, roundingY)

    #########################
    ## Selection

    def isSelected(self):
        return self.__selected

    def setSelected(self, selected=True):
        self.__selected = selected
        self.update()


    #########################
    ## Graph Pos

    def getGraphPos(self):
        transform = self.transform()
        size = self.size()
        return QtCore.QPointF(transform.dx()+(size.width()*0.5), transform.dy()+(size.height()*0.5))


    def setGraphPos(self, graphPos):
        size = self.size()
        self.setTransform(QtGui.QTransform.fromTranslate(graphPos.x()-(size.width()*0.5), graphPos.y()-(size.height()*0.5)), False)


    def pushGraphPosToComponent(self):
        graphPos = self.getGraphPos()
        self.__component.setGraphPos( Vec2(graphPos.x(), graphPos.y()) )


    #########################
    ## Events

    def mousePressEvent(self, event):
        if event.button() is QtCore.Qt.MouseButton.LeftButton:

            modifiers = event.modifiers()
            if modifiers == QtCore.Qt.ControlModifier:
                if self.isSelected() is False:
                    self.__graph.selectNode(self, clearSelection=False)
                else:
                    self.__graph.deselectNode(self)

            elif modifiers == QtCore.Qt.ShiftModifier:
                if self.isSelected() is False:
                    self.__graph.selectNode(self, clearSelection=False)
            else:
                if self.isSelected() is False: # and len(self.__graph.getSelectedNodes()) == 0:
                    # self.__graph.selectNode(self, clearSelection=True)
                    UndoRedoManager.getInstance().addCommand(SelectNodeCommand(self.__graph, self))

                self.__dragging = True
                self._lastDragPoint = self.mapToItem(self.__graph.itemGroup(), event.pos())


        else:
            super(Node, self).mousePressEvent(event)


    def mouseMoveEvent(self, event):
        if self.__dragging:
            newPos = self.mapToItem(self.__graph.itemGroup(), event.pos())
            delta = newPos - self._lastDragPoint
            self._lastDragPoint = newPos

            if not self.isSelected():
                self.translate(delta.x(), delta.y())
            else:
                selectedNodes = self.__graph.getSelectedNodes()
                # Apply the delta to each selected key
                for node in selectedNodes:
                    node.translate(delta.x(), delta.y())
        else:
            super(Node, self).mouseMoveEvent(event)


    def mouseReleaseEvent(self, event):
        if self.__dragging:
                # TODO: Undo code goes here...
            if not self.isSelected():
                self.pushGraphPosToComponent()

            else:
                selectedNodes = self.__graph.getSelectedNodes()
                for node in selectedNodes:
                    node.pushGraphPosToComponent()

            self.setCursor(QtCore.Qt.ArrowCursor)
            self.__dragging = False
        else:
            super(Node, self).mouseReleaseEvent(event)


    def mouseDoubleClickEvent(self, event):
        if self.__inspectorWidget is None:
            parentWidget = self.__graph.graphView().getGraphViewWidget()
            self.__inspectorWidget = ComponentInspector(component=self.__component, parent=parentWidget, nodeItem=self)
            self.__inspectorWidget.show()
        else:
            self.__inspectorWidget.setFocus()

        super(Node, self).mouseDoubleClickEvent(event)


    def inspectorClosed(self):
        self.__inspectorWidget = None


    def nameChanged(self, origName):
        self.__titleItem.setText(self.__component.getDecoratedName())
        self.__graph.nodeNameChanged(origName, self.__component.getDecoratedName())

        # Update the node so that the size is computed.
        self.adjustSize()

    #########################
    ## shut down

    def destroy(self):
        for port in self.__inports:
            port.destroy()

        for port in self.__outports:
            port.destroy()

        self.scene().removeItem(self)
