
#
# Copyright 2010-2015
#

#pylint: disable-msg=W0613
import json
from PySide import QtGui, QtCore
from port import InputPort, OutputPort
from kraken.core.maths import Vec2

from kraken.ui.component_inspector import ComponentInspector


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


class PortList(QtGui.QGraphicsWidget):
    def __init__(self, parent):
        super(PortList, self).__init__(parent)
        layout = QtGui.QGraphicsLinearLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(7)
        layout.setOrientation(QtCore.Qt.Vertical)
        self.setLayout(layout)

    def addPort(self, port, alignment):
        layout = self.layout()
        layout.addItem(port)
        layout.setAlignment(port, alignment)
        self.adjustSize()
        return port


class Node(QtGui.QGraphicsWidget):

    nameChanged = QtCore.Signal(str, str)

    __defaultColor = QtGui.QColor(154, 205, 50, 255)
    __unselectedPen =  QtGui.QPen(QtGui.QColor(25, 25, 25), 1.6)
    __selectedPen =  QtGui.QPen(QtGui.QColor(255, 255, 255, 255), 1.6)
    __linePen =  QtGui.QPen(QtGui.QColor(25, 25, 25, 255), 1.25)

    def __init__(self, graph, component):
        super(Node, self).__init__()

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
        self.__inputPortsHolder = PortList(self)
        self.__outputPortsHolder = PortList(self)



        layout.addItem(self.__inputPortsHolder)

        # Insert space between input and output ports
        spacingWidget = QtGui.QGraphicsWidget(self)
        spacingWidget.setPreferredSize(2.0, 2.0)
        layout.addItem(spacingWidget)
        layout.addItem(self.__outputPortsHolder)

        self.__selected = False
        self.__dragging = False


        def getPortColor(dataType):

            if dataType.startswith('Xfo'):
                return QtGui.QColor(128, 170, 170, 255)
            elif dataType.startswith('Float'):
                return QtGui.QColor(32, 255, 32, 255)
            elif dataType.startswith('Integer'):
                return QtGui.QColor(0, 128, 0, 255)
            elif dataType.startswith('Boolean'):
                return QtGui.QColor(255, 102, 0, 255)
            else:
                return QtGui.QColor(50, 205, 254, 255)

        for i in range(self.__component.getNumInputs()):
            componentInput = component.getInputByIndex(i)
            name = componentInput.getName()
            dataType = componentInput.getDataType()
            color = getPortColor(dataType)

            self.addInputPort(InputPort(self, graph, name, color, dataType))

        for i in range(self.__component.getNumOutputs()):
            componentOutput = component.getOutputByIndex(i)
            name = componentOutput.getName()
            dataType = componentOutput.getDataType()
            color = getPortColor(dataType)

            self.addOutputPort(OutputPort(self, graph, name, color, dataType))

        self.setGraphPos( QtCore.QPointF( self.__component.getGraphPos().x, self.__component.getGraphPos().y ) )


    def getName(self):
        return self.__component.getDecoratedName()

    def getComponent(self):
        return self.__component

    def getGraph(self):
        return self.__graph

    #########################
    ## Ports

    def addInputPort(self, port):
        self.__inputPortsHolder.addPort(port, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.__inports.append(port)
        self.adjustSize()
        return port

    def addOutputPort(self, port):
        self.__outputPortsHolder.addPort(port, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
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
                if self.isSelected() is False:
                    self.__graph.selectNode(self, clearSelection=False)

                self.__dragging = True
                self._mouseDownPoint = self.mapToScene(event.pos())
                self._lastDragPoint = self._mouseDownPoint

        else:
            super(Node, self).mousePressEvent(event)


    def mouseMoveEvent(self, event):
        if self.__dragging:
            newPos = self.mapToScene(event.pos())
            delta = newPos - self._lastDragPoint
            self.__graph.moveSelectedNodes(delta)
            self._lastDragPoint = newPos
        else:
            super(Node, self).mouseMoveEvent(event)


    def mouseReleaseEvent(self, event):
        if self.__dragging:

            newPos = self.mapToScene(event.pos())
            delta = newPos - self._mouseDownPoint
            self.__graph.endMoveSelectedNodes(delta)

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

    def disconnectAllPorts(self):
        for port in self.__inports:
            port.disconnect()

        for port in self.__outports:
            port.disconnect()

    # def destroy(self):
    #     for port in self.__inports:
    #         port.destroy()

    #     for port in self.__outports:
    #         port.destroy()

    #     self.scene().removeItem(self)
