
#
# Copyright 2010-2015
#

from PySide import QtGui, QtCore
from port import PortCircle, PortLabel
from connection import Connection

class MouseGrabber(PortCircle):
    """docstring for MouseGrabber"""

    def __init__(self, graph, pos, otherPortCircle, connectionPointType):
        super(MouseGrabber, self).__init__(None, graph, 0, otherPortCircle.getPort().getColor(), connectionPointType)

        self._ellipseItem.setPos(0, 0)
        self._ellipseItem.setStartAngle(0)
        self._ellipseItem.setSpanAngle(360 * 16)

        self.__otherPortItem = otherPortCircle

        self._graph.scene().addItem(self)


        self.setZValue(-1)
        self.setTransform(QtGui.QTransform.fromTranslate(pos.x(), pos.y()), False)
        self.grabMouse()

        import connection
        if self.connectionPointType() == 'Out':
            self.__connection = connection.Connection(self._graph, self, otherPortCircle)
        elif self.connectionPointType() == 'In':
            self.__connection = connection.Connection(self._graph, otherPortCircle, self)
        # Do not emit a notification for this temporary connection.
        self._graph.addConnection(self.__connection, emitSignal=False)
        self.__mouseOverPortItem = None
        self._graph.emitBeginConnectionManipulationSignal()


    def getColor(self):
        return self.__otherPortItem.getPort().getColor()


    def mouseMoveEvent(self, event):
        scenePos = self.mapToScene(event.pos())
        self.setTransform(QtGui.QTransform.fromTranslate(scenePos.x(), scenePos.y()), False)

        collidingItems = self.collidingItems(QtCore.Qt.IntersectsItemBoundingRect)
        collidingPortCircles = filter(lambda item: isinstance(item, (PortCircle, PortLabel)), collidingItems)

        def canConnect(item):
            if isinstance(item, (PortCircle, PortLabel)):
                mouseOverPortItem = item
            else:
                if self.connectionPointType() == 'In':
                    mouseOverPortItem = item.getPort().inCircle()
                else:
                    mouseOverPortItem = item.getPort().outCircle()

                if mouseOverPortItem == None:
                    return False

            if self.connectionPointType() != mouseOverPortItem.connectionPointType():
                return False

            if mouseOverPortItem.getPort().getDataType() != self.__otherPortItem.getPort().getDataType():
                return False

            # Check if you're trying to connect to the
            mouseOverPort = mouseOverPortItem.getPort()
            otherPort = self.__otherPortItem.getPort()
            if mouseOverPort.getNode() == otherPort.getNode():
                return False

            return True

        collidingPortCircles = filter(lambda port: canConnect(port), collidingPortCircles)
        if len(collidingPortCircles) > 0:
            if self.__mouseOverPortItem and self.__mouseOverPortItem != collidingPortCircles[0]:
                self.__mouseOverPortItem.unhighlight()

            if isinstance(collidingPortCircles[0], (PortCircle, PortLabel)):
                self.__mouseOverPortItem = collidingPortCircles[0]
            else:
                if self.connectionPointType() == 'In':
                    self.__mouseOverPortItem = collidingPortCircles[0].getPort().inCircle()
                else:
                    self.__mouseOverPortItem = collidingPortCircles[0].getPort().outCircle()

            self.__mouseOverPortItem.highlight()
        elif self.__mouseOverPortItem != None:
            self.__mouseOverPortItem.unhighlight()
            self.__mouseOverPortItem = None


    def mouseReleaseEvent(self, event):

        if self.__mouseOverPortItem is not None:
            self.__mouseOverPortItem.unhighlight()
            try:

                if self.connectionPointType() == 'In':
                    if isinstance(self.__otherPortItem, PortLabel):
                        sourcePortCircle = self.__otherPortItem.getPortCircle()
                    else:
                        sourcePortCircle = self.__otherPortItem

                    if isinstance(self.__mouseOverPortItem, PortLabel):
                        targetPortCircle = self.__mouseOverPortItem.getPortCircle()
                    else:
                        targetPortCircle = self.__mouseOverPortItem
                elif self.connectionPointType() == 'Out':
                    if isinstance(self.__mouseOverPortItem, PortLabel):
                        sourcePortCircle = self.__mouseOverPortItem.getPortCircle()
                    else:
                        sourcePortCircle = self.__mouseOverPortItem

                    if isinstance(self.__otherPortItem, PortLabel):
                        targetPortCircle = self.__otherPortItem.getPortCircle()
                    else:
                        targetPortCircle = self.__otherPortItem

                from connection import Connection
                connection = Connection(self._graph, sourcePortCircle, targetPortCircle)
                self._graph.addConnection(connection)
                self._graph.emitEndConnectionManipulationSignal()

            except Exception as e:
                print "Exception in MouseGrabber.mouseReleaseEvent: " + str(e)

        self.destroy()



    # def paint(self, painter, option, widget):
    #     super(MouseGrabber, self).paint(painter, option, widget)
    #     painter.setPen(QtGui.QPen(self.getColor()))
    #     painter.drawRect(self.windowFrameRect())

    def destroy(self):
        self.ungrabMouse()
        scene = self.scene()
        # Destroy the temporary connection.
        self._graph.removeConnection(self.__connection, emitSignal=False)
        # Destroy the grabber.
        scene.removeItem(self)
        scene.update()

