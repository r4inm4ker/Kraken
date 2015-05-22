
#
# Copyright 2010-2015
#

#pylint: disable-msg=W0613
import json
from PySide import QtGui, QtCore
from mouse_grabber import MouseGrabber

class PortLabel(QtGui.QGraphicsWidget):
    __font = QtGui.QFont('Decorative', 14)

    def __init__(self, parent, text, hOffset, color):
        super(PortLabel, self).__init__(parent)
        self.__text = text
        self.__textItem = QtGui.QGraphicsTextItem(text, self)
        self.__textItem.setDefaultTextColor(color)
        self.__textItem.setFont(self.__font)
        self.__textItem.translate( hOffset, -8)
        option=self.__textItem.document().defaultTextOption()
        option.setWrapMode(QtGui.QTextOption.NoWrap)
        self.__textItem.document().setDefaultTextOption(option)
        self.__textItem.adjustSize()

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

    # def paint(self, painter, option, widget):
    #     super(PortLabel, self).paint(painter, option, widget)
    #     painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 255)))
    #     painter.drawRect(self.windowFrameRect())


class PortCircle(QtGui.QGraphicsWidget):
    __radius = 4
    __diameter = 2 * __radius

    def __init__(self, port, graph, connectionPointType, hOffset, color):
        super(PortCircle, self).__init__(port)

        self.__port = port
        self.__graph = graph
        self.__connectionPointType = connectionPointType

        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed))
        size = QtCore.QSizeF(
            self.__diameter * 2,
            self.__diameter * 2,
            )
        self.setPreferredSize(size)
        self.setWindowFrameMargins(0, 0, 0, 0)
        self.translate(hOffset, 0)

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

    def unhighlight(self):
        self.__ellipseItem.setBrush(QtGui.QBrush(self.__color))

    def hoverEnterEvent(self, event):
        self.highlight()
        super(PortCircle, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.unhighlight()
        super(PortCircle, self).hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        scenePos = self.mapToItem(self.__graph.itemGroup(), event.pos())

        self.unhighlight()
        if self.__connectionPointType == 'In':
            self.__graph.controller().beginInteraction("Edit connection to:" + self.__port.getPath())
            MouseGrabber(self.__graph, scenePos, self.__port, 'Out')
        elif self.__connectionPointType == 'Out':
            self.__graph.controller().beginInteraction("Edit connections from:" + self.__port.getPath())
            MouseGrabber(self.__graph, scenePos, self.__port, 'In')

    # def paint(self, painter, option, widget):
    #     super(PortCircle, self).paint(painter, option, widget)
    #     painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 0)))
    #     painter.drawRect(self.windowFrameRect())


class BasePort(QtGui.QGraphicsWidget):
    def __init__(self, parent, graph, label, color, connectionPointType, labelColor):
        super(BasePort, self).__init__(parent)

        self.__graph = graph
        self.__label = label
        self.__labelColor = labelColor

        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed))

        layout = QtGui.QGraphicsLinearLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)
        self.setLayout(layout)

        self.__color = color
        self.__inCircle = None
        self.__outCircle = None

        if connectionPointType in ["In", "IO"]:
            self.__inCircle = PortCircle(self, self.__graph, 'In', -10, self.__color)
            layout.addItem(self.__inCircle)
            layout.setAlignment(self.__inCircle, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        if connectionPointType != "In":
            layout.addStretch(2)

        # Because the port circle is offset, we also offset the label by the same amount.
        labelHOffset = 0
        if connectionPointType == "In":
            labelHOffset = -10
        elif connectionPointType == "Out":
            labelHOffset = 10

        if self.__label != "":
            self.__labelItem = PortLabel(self, self.__label, labelHOffset, self.__labelColor)
            layout.addItem(self.__labelItem)
            layout.setAlignment(self.__labelItem, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        if connectionPointType != "Out":
            layout.addStretch(2)

        if connectionPointType in ["Out", "IO"]:
            self.__outCircle = PortCircle(self, self.__graph, 'Out', 10, self.__color)
            layout.addItem(self.__outCircle)
            layout.setAlignment(self.__outCircle, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def inCircle(self):
        if self.__inCircle is None:
            raise Exception("Port '" + self.__label + "' Does not have an 'In' connection point.");
        return self.__inCircle

    def outCircle(self):
        if self.__outCircle is None:
            raise Exception("Port '" + self.__label + "' Does not have an 'Out' connection point.");
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
        self.scene().removeItem(self)



# class PortFromDesc(BasePort):
#     def __init__(self, parent, graph, desc, connectionPointType = None, labelColor = QtGui.QColor(25, 25, 25)):

#         self.__graph = graph
#         self.__portDesc = desc
#         print

#         label = self.__portDesc['title']
#         print "parent:" + str(parent)
#         print "PortFromDesc:" + str(desc)
#         if 'type' in desc:
#             color = self.__graph.controller().getDataTypeColor(self.__portDesc['type'])
#         else:
#             color = self.__graph.controller().getDataTypeColor(None)

#         if connectionPointType is None:
#             connectionPointType = self.__portDesc['portType']

#         super(PortFromDesc, self).__init__(parent, graph, label, color, connectionPointType, labelColor)

#     def getPath(self):
#         raise Exception("getPath not yet supported")
#         # return self.__path

#     def getName(self):
#         return self.__portDesc['name']

#     def getDataType(self):
#         return self.__portDesc['type']



class PortFromPath(BasePort):
    def __init__(self, parent, graph, path, connectionPointType = None, labelColor = QtGui.QColor(25, 25, 25)):

        self.parent = parent
        self.__graph = graph
        self.__path = path
        self.__portDesc = self.__graph.controller().getDesc(path=self.__path)
        self.__evalDesc = parent.getPortEvalDesc(self.__portDesc['name'])
        self.__dataType = None

        if self.__evalDesc is not None and 'type' in self.__evalDesc:
            self.__dataType = self.__evalDesc['type']
        elif 'dataType' in self.__portDesc:
            self.__dataType = self.__portDesc['dataType']

        label = self.__portDesc['title']
        color = self.__graph.controller().getDataTypeColor(self.__dataType)

        if connectionPointType is None:
            connectionPointType = self.__portDesc['connectionPointType']

        super(PortFromPath, self).__init__(parent, graph, label, color, connectionPointType, labelColor)

        self.__graph.controller().addNotificationListener('scene.bindingChanged', self.__bindingChanged)

    def getPath(self):
        return self.__path

    def getName(self):
        return self.__portDesc['name']

    def getDataType(self):
        return self.__dataType

    def __bindingChanged(self, data):
        self.__evalDesc = self.parent.getPortEvalDesc(self.__portDesc['name'])
        self.__dataType = None
        if self.__evalDesc is not None and 'type' in self.__evalDesc:
            self.__dataType = self.__evalDesc['type']
        self.setColor(self.__graph.controller().getDataTypeColor(self.__dataType))


    def destroy(self):
        self.__graph.controller().removeNotificationListener('scene.bindingChanged', self.__bindingChanged)
        self.scene().removeItem(self)

