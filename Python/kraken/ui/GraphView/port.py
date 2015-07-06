
#
# Copyright 2010-2015
#

#pylint: disable-msg=W0613
import json
from PySide import QtGui, QtCore
from mouse_grabber import MouseGrabber

class PortLabel(QtGui.QGraphicsWidget):
    __font = QtGui.QFont('Decorative', 12)

    def __init__(self, port, text, connectionPointType, hOffset, color, highlightColor):
        super(PortLabel, self).__init__(port)
        self.__port = port
        self.__text = text
        self.__textItem = QtGui.QGraphicsTextItem(text, self)
        self.__labelColor = color
        self.__highlightColor = highlightColor
        self.__textItem.setDefaultTextColor(self.__labelColor)
        self.__textItem.setFont(self.__font)
        self.__textItem.translate(hOffset, -8)
        option = self.__textItem.document().defaultTextOption()
        option.setWrapMode(QtGui.QTextOption.NoWrap)
        self.__textItem.document().setDefaultTextOption(option)
        self.__textItem.adjustSize()

        self.__connectionPointType = connectionPointType

        self.setAcceptHoverEvents(True)
        self.setPreferredSize(self.textSize())
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed))
        self.setWindowFrameMargins(0, 0, 0, 0)

    def text(self):
        return self.__text

    def setColor(self, color):
        self.__textItem.setDefaultTextColor(color)
        self.update()

    def textSize(self):
        return QtCore.QSizeF(
            self.__textItem.textWidth(),
            self.__font.pointSizeF()
            )

    def getPort(self):
        return self.__port

    def connectionPointType(self):
        return self.__connectionPointType

    def isInConnectionPoint(self):
        return self.__connectionPointType == 'In'

    def isOutConnectionPoint(self):
        return self.__connectionPointType == 'Out'

    # def paint(self, painter, option, widget):
    #     super(PortLabel, self).paint(painter, option, widget)
    #     painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 255)))
    #     painter.drawRect(self.windowFrameRect())

    def highlight(self):
        self.setColor(self.__highlightColor)

    def unhighlight(self):
        self.setColor(self.__labelColor)

    def hoverEnterEvent(self, event):
        self.highlight()
        super(PortLabel, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.unhighlight()
        super(PortLabel, self).hoverLeaveEvent(event)

    def mousePressEvent(self, event):

        scenePos = self.mapToItem(self.getPort().getGraph().itemGroup(), event.pos())

        #self.unhighlight()
        if self.isInConnectionPoint():
        #     self.__graph.controller().beginInteraction("Edit connection to:" + self.__port.getPath())
            MouseGrabber(self.getPort().getGraph(), scenePos, self.__port, 'Out')
        elif self.isOutConnectionPoint():
        #     self.__graph.controller().beginInteraction("Edit connections from:" + self.__port.getPath())
            MouseGrabber(self.getPort().getGraph(), scenePos, self.__port, 'In')


class PortCircle(QtGui.QGraphicsWidget):
    __radius = 4.5
    __diameter = 2 * __radius

    def __init__(self, port, graph, connectionPointType, color):
        super(PortCircle, self).__init__(port)

        self.__port = port
        self.__graph = graph
        self.__connectionPointType = connectionPointType

        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed))
        size = QtCore.QSizeF(self.__diameter, self.__diameter)
        self.setPreferredSize(size)
        self.setWindowFrameMargins(0, 0, 0, 0)

        if self.isInConnectionPoint():
            self.translate(self.__radius * -2, 0)
        else:
            self.translate(self.__radius * 2, 0)

        self.__defaultPen = QtGui.QPen(QtGui.QColor(25, 25, 25), 1.0)
        self.__hoverPen = QtGui.QPen(QtGui.QColor(255, 255, 100), 1.5)
        self.setAcceptHoverEvents(True)

        self.__ellipseItem = QtGui.QGraphicsEllipseItem()
        self.__ellipseItem.setPen(self.__defaultPen)
        self.__ellipseItem.setPos(size.width()/2, size.height()/2)
        self.__ellipseItem.setRect(
            -self.__radius,
            -self.__radius,
            self.__diameter,
            self.__diameter,
            )
        if self.isInConnectionPoint():
            self.__ellipseItem.setStartAngle(270 * 16)
            self.__ellipseItem.setSpanAngle(180 * 16)
        self.__ellipseItem.setParentItem(self)
        self.setColor(color)

    def getPort(self):
        return self.__port

    def connectionPointType(self):
        return self.__connectionPointType

    def isInConnectionPoint(self):
        return self.__connectionPointType == 'In'

    def isOutConnectionPoint(self):
        return self.__connectionPointType == 'Out'

    def centerInSceneCoords(self):
        return self.__ellipseItem.mapToScene(0, 0)

    def setColor(self, color):
        self.__color = color
        self.__ellipseItem.setBrush(QtGui.QBrush(self.__color))

    def highlight(self):
        self.__ellipseItem.setBrush(QtGui.QBrush(self.__color.lighter()))
        # make the port bigger to highliht it can accept the connection.
        self.__ellipseItem.setRect(
            -self.__radius * 1.6,
            -self.__radius * 1.6,
            self.__diameter * 1.6,
            self.__diameter * 1.6,
            )

    def unhighlight(self):
        self.__ellipseItem.setBrush(QtGui.QBrush(self.__color))
        self.__ellipseItem.setRect(
            -self.__radius,
            -self.__radius,
            self.__diameter,
            self.__diameter,
            )

    def hoverEnterEvent(self, event):
        self.highlight()
        super(PortCircle, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.unhighlight()
        super(PortCircle, self).hoverLeaveEvent(event)

    def mousePressEvent(self, event):

        scenePos = self.mapToItem(self.__graph.itemGroup(), event.pos())

        self.unhighlight()

        if self.isInConnectionPoint():
            grabber = MouseGrabber(self.__graph, scenePos, self.__port, 'Out')

        elif self.isOutConnectionPoint():
            grabber = MouseGrabber(self.__graph, scenePos, self.__port, 'In')

    # def paint(self, painter, option, widget):
    #     super(PortCircle, self).paint(painter, option, widget)
    #     painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 0)))
    #     painter.drawRect(self.windowFrameRect())


class BasePort(QtGui.QGraphicsWidget):
    def __init__(self, parent, graph, componentInput, connectionPointType):
        super(BasePort, self).__init__(parent)

        self.__node = parent
        self.__graph = graph
        self.__componentInput = componentInput
        self.__connections = []

        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed))

        layout = QtGui.QGraphicsLinearLayout()
        layout.setSpacing(0)
        self.setLayout(layout)

        if self.getDataType().startswith('Xfo'):
            self.__color = QtGui.QColor(128, 170, 170, 255)
        elif self.getDataType().startswith('Float'):
            self.__color = QtGui.QColor(32, 255, 32, 255)
        elif self.getDataType().startswith('Integer'):
            self.__color = QtGui.QColor(0, 128, 0, 255)
        elif self.getDataType().startswith('Boolean'):
            self.__color = QtGui.QColor(255, 102, 0, 255)
        else:
            self.__color = QtGui.QColor(50, 205, 254, 255)

        self.__labelColor = QtGui.QColor(25, 25, 25)
        self.__labelHighlightColor = self.__color.lighter(200)
        self.__label = self.__componentInput.getName()
        self.__inCircle = None
        self.__outCircle = None

        if connectionPointType in ["In", "IO"]:
            self.__inCircle = PortCircle(self, self.__graph, 'In', self.__color)
            layout.addItem(self.__inCircle)
            layout.setAlignment(self.__inCircle, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        # Pushes the out port to the side
        if connectionPointType != "In":
            layout.addStretch(2)

        # Because the port circle is offset, we also offset the label by the same amount.
        labelHOffset = 0
        if connectionPointType == "In":
            layout.setContentsMargins(0, 0, 30, 0)
            labelHOffset = -10
        elif connectionPointType == "Out":
            layout.setContentsMargins(30, 0, 0, 0)
            labelHOffset = 10

        if self.__label != "":
            self.__labelItem = PortLabel(self, self.__label, connectionPointType, labelHOffset, self.__labelColor, self.__labelHighlightColor)
            layout.addItem(self.__labelItem)
            layout.setAlignment(self.__labelItem, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        if connectionPointType != "Out":
            layout.addStretch(2)

        if connectionPointType in ["Out", "IO"]:
            self.__outCircle = PortCircle(self, self.__graph, 'Out', self.__color)
            layout.addItem(self.__outCircle)
            layout.setAlignment(self.__outCircle, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def getName(self):
        return self.__componentInput.getName()

    def getDataType(self):
        return self.__componentInput.getDataType()

    def getNode(self):
        return self.__node

    def getGraph(self):
        return self.__graph

    # ===================
    # Connection Methods
    # ===================
    def addConnection(self, connection):
        """Adds a connection to the list.

        Arguments:
        connection -- connection, new connection to add.

        Return:
        True if successful.

        """

        self.__connections.append(connection)

        return True

    def removeConnection(self, connection):
        """Removes a connection to the list.

        Arguments:
        connection -- connection, connection to remove.

        Return:
        True if successful.

        """

        deleteIndex = None
        for i, conn in enumerate(self.__connections):
            if conn == connection:
                deleteIndex = i
                break

        if deleteIndex is not None:
            del self.__connections[deleteIndex]
        
        return True

    def getConnections(self):
        """Gets the ports connections list.

        Return:
        List, connections to this port.

        """

        return self.__connections


    def inCircle(self):
        if self.__inCircle is None:
            raise Exception("Port '" + self.getNode().getName() + "." + self.__label + "' Does not have an 'In' connection point.");
        return self.__inCircle

    def outCircle(self):
        if self.__outCircle is None:
            raise Exception("Port '" + self.getNode().getName() + "." + self.__label + "' Does not have an 'Out' connection point.");
        return self.__outCircle

    def getColor(self):
        return self.__color

    def setColor(self, color):
        if self.__inCircle is not None:
            self.__inCircle.setColor(color)
        if self.__outCircle is not None:
            self.__outCircle.setColor(color)
        self.__color = color

    # def paint(self, painter, option, widget):
    #     super(BasePort, self).paint(painter, option, widget)
    #     painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 0)))
    #     painter.drawRect(self.windowFrameRect())

    def destroy(self):

        for connection in self.getConnections():
            connection.destroy()

        self.scene().removeItem(self)


class InputPort(BasePort):
    """docstring for InputPort"""
    def __init__(self, parent, graph, componentInput):
        super(InputPort, self).__init__(parent, graph, componentInput, 'In')


class OutputPort(BasePort):
    """docstring for OutputPort"""
    def __init__(self, parent, graph, componentOutput):
        super(OutputPort, self).__init__(parent, graph, componentOutput, 'Out')
