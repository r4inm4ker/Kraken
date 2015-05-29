
#
# Copyright 2010-2015
#

#pylint: disable-msg=W0613

from PySide import QtGui, QtCore


class MouseGrabber(QtGui.QGraphicsWidget):
    """docstring for MouseGrabber"""
    __radius = 1
    __diameter = 2 * __radius
    def __init__(self, graph, pos, port, connectionPointType):
        super(MouseGrabber, self).__init__(graph.itemGroup())
        self.__graph = graph
        self.__port = port
        self.__connectionPointType = connectionPointType

        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed))
        size = QtCore.QSizeF(
            self.__diameter * 2,
            self.__diameter * 2,
            )
        self.setPreferredSize(size)
        self.setPos(-self.__diameter, -self.__diameter)
        self.setWindowFrameMargins(0, 0, 0, 0)

        self.setZValue(-1)
        self.setTransform(QtGui.QTransform.fromTranslate(pos.x(), pos.y()), False)
        self.grabMouse()

        import connection
        if self.__connectionPointType == 'Out':
            self.__connection = connection.Connection(self.__graph, self, port)
        elif self.__connectionPointType == 'In':
            self.__connection = connection.Connection(self.__graph, port, self)

        self.__mouseOverPortCircle = None

    def inCircle(self):
        return self

    def outCircle(self):
        return self

    def getColor(self):
        return self.__port.getColor()

    def centerInSceneCoords(self):
        return self.mapToScene(self.__diameter, self.__diameter)

    def mouseMoveEvent(self, event):
        scenePos = self.mapToItem(self.__graph.itemGroup(), event.pos())
        self.setTransform(QtGui.QTransform.fromTranslate(scenePos.x(), scenePos.y()), False)

        import port
        collidingItems = self.collidingItems(QtCore.Qt.IntersectsItemBoundingRect)
        collidingPortCircles = filter(lambda item: isinstance(item, port.PortCircle), collidingItems)

        def canConnect(mouseOverPortCircle):
            if self.__connectionPointType != mouseOverPortCircle.connectionPointType():
                return False
            # print " self DataType:" + self.__port.getDataType()
            # print " mouseOverPortCircle DataType:" + mouseOverPortCircle.getPort().getDataType()
            # if self.__port.getDataType() != mouseOverPortCircle.getPort().getDataType():
            #     return False
            return True

        collidingPortCircles = filter(lambda port: canConnect(port), collidingPortCircles)
        if len(collidingPortCircles) > 0:
            if self.__mouseOverPortCircle and self.__mouseOverPortCircle != collidingPortCircles[0]:
                self.__mouseOverPortCircle.unhighlight()
            self.__mouseOverPortCircle = collidingPortCircles[0]
            self.__mouseOverPortCircle.highlight()
        elif self.__mouseOverPortCircle != None:
            self.__mouseOverPortCircle.unhighlight()
            self.__mouseOverPortCircle = None

    def mouseReleaseEvent(self, event):
        self.ungrabMouse()
        graph = self.__graph
        scene = self.scene()
        # Destroy the temporary connection.
        scene.removeItem(self.__connection)
        # Destroy the grabber.
        scene.removeItem(self)
        scene.update()

        if self.__mouseOverPortCircle is not None:
            self.__mouseOverPortCircle.unhighlight()
            try:

                if self.__connectionPointType == 'In':
                    sourcePort = self.__port
                    targetPort = self.__mouseOverPortCircle.getPort()
                elif self.__connectionPointType == 'Out':
                    sourcePort = self.__mouseOverPortCircle.getPort()
                    targetPort = self.__port

                sourceComponent = sourcePort.getNode().getComponent()
                targetComponent = targetPort.getNode().getComponent()

                rig = self.__graph.getRig()

                sourceComponentOutputPort = sourceComponent.getOutputByName(sourcePort.getName())
                targetComponentInputPort = targetComponent.getInputByName(targetPort.getName())
                targetComponentInputPort.setConnection(sourceComponentOutputPort)

                connectionJson = {
                    'source': sourceComponent.getName() + '.' + sourceComponentOutputPort.getName(),
                    'target': targetComponent.getName() + '.' + targetComponentInputPort.getName()
                }
                self.__graph.addConnection(connectionJson)

            except Exception as e:
                print "Exception in MouseGrabber.mouseReleaseEvent: " + str(e)




    def paint(self, painter, option, widget):
        super(MouseGrabber, self).paint(painter, option, widget)
        painter.setPen(QtGui.QPen(self.getColor()))
        painter.drawRect(self.windowFrameRect())
