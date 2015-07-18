
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

        self.__otherPortCircle = otherPortCircle

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
        self.__mouseOverPortCircle = None
        self._graph.emitBeginConnectionManipulationSignal()


    def getColor(self):
        return self.__otherPortCircle.getPort().getColor()


    def mouseMoveEvent(self, event):
        scenePos = self.mapToScene(event.pos())
        self.setTransform(QtGui.QTransform.fromTranslate(scenePos.x(), scenePos.y()), False)

        collidingItems = self.collidingItems(QtCore.Qt.IntersectsItemBoundingRect)
        collidingPortCircles = filter(lambda item: isinstance(item, (PortCircle, PortLabel)), collidingItems)

        def canConnect(item):
            if isinstance(item, (PortCircle, PortLabel)):
                mouseOverPortCircle = item
            else:
                if self.connectionPointType() == 'In':
                    mouseOverPortCircle = item.getPort().inCircle()
                else:
                    mouseOverPortCircle = item.getPort().outCircle()

                if mouseOverPortCircle == None:
                    return False

            if self.connectionPointType() != mouseOverPortCircle.connectionPointType():
                return False

            if mouseOverPortCircle.getPort().getDataType() != self.__otherPortCircle.getPort().getDataType():
                return False

            # Check if you're trying to connect to the
            mouseOverPort = mouseOverPortCircle.getPort()
            otherPort = self.__otherPortCircle.getPort()
            if mouseOverPort.getNode() == otherPort.getNode():
                return False

            return True

        collidingPortCircles = filter(lambda port: canConnect(port), collidingPortCircles)
        if len(collidingPortCircles) > 0:
            if self.__mouseOverPortCircle and self.__mouseOverPortCircle != collidingPortCircles[0]:
                self.__mouseOverPortCircle.unhighlight()

            if isinstance(collidingPortCircles[0], (PortCircle, PortLabel)):
                self.__mouseOverPortCircle = collidingPortCircles[0]
            else:
                if self.connectionPointType() == 'In':
                    self.__mouseOverPortCircle = collidingPortCircles[0].getPort().inCircle()
                else:
                    self.__mouseOverPortCircle = collidingPortCircles[0].getPort().outCircle()

            self.__mouseOverPortCircle.highlight()
        elif self.__mouseOverPortCircle != None:
            self.__mouseOverPortCircle.unhighlight()
            self.__mouseOverPortCircle = None


    def mouseReleaseEvent(self, event):

        if self.__mouseOverPortCircle is not None:
            self.__mouseOverPortCircle.unhighlight()
            try:

                if self.connectionPointType() == 'In':
                    sourcePortCircle = self.__otherPortCircle

                    if isinstance(self.__mouseOverPortCircle, PortLabel):
                        targetPortCircle = self.__mouseOverPortCircle.getPortCircle()
                    else:
                        targetPortCircle = self.__mouseOverPortCircle
                elif self.connectionPointType() == 'Out':
                    sourcePortCircle = self.__mouseOverPortCircle

                    if isinstance(self.__mouseOverPortCircle, PortLabel):
                        targetPortCircle = self.__mouseOverPortCircle.getPortCircle()
                    else:
                        targetPortCircle = self.__otherPortCircle

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

