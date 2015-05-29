
#
# Copyright 2010-2015
#

#pylint: disable-msg=W0613
import json
from PySide import QtGui, QtCore
from port import InputPort, OutputPort
# from FabricEngine.DFG.Widgets.node_inspector import NodeInspectorDockWidget

class NodeTitle(QtGui.QGraphicsWidget):
    __color = QtGui.QColor(25, 25, 25)
    __font = QtGui.QFont('Decorative', 16)

    def __init__(self, text, parent=None):
        super(NodeTitle, self).__init__(parent)

        self.__textItem = QtGui.QGraphicsTextItem(text, self)
        self.__textItem.setDefaultTextColor(self.__color)
        self.__textItem.setFont(self.__font)
        self.__textItem.setPos(0, -4)
        option=self.__textItem.document().defaultTextOption()
        option.setWrapMode(QtGui.QTextOption.NoWrap)
        self.__textItem.document().setDefaultTextOption(option)
        self.__textItem.adjustSize()

        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed))
        self.setPreferredSize(self.textSize())

    def textSize(self):
        return QtCore.QSizeF(
            self.__textItem.textWidth(),
            self.__font.pointSizeF()
            )

    def paint(self, painter, option, widget):
        super(NodeTitle, self).paint(painter, option, widget)
        # painter.setPen(QtGui.QPen(QtGui.QColor(0, 255, 0)))
        # painter.drawRect(self.windowFrameRect())


class Node(QtGui.QGraphicsWidget):
    __defaultColor = QtGui.QColor(154, 205, 50, 255)
    __unselectedPen =  QtGui.QPen(QtGui.QColor(25, 25, 25), 1.6)
    __selectedPen =  QtGui.QPen(QtGui.QColor(255, 255, 255, 255), 1.6)

    def __init__(self, graph, component):
        super(Node, self).__init__(graph.itemGroup())

        self.setMinimumWidth(60)
        self.setMinimumHeight(20)
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))

        layout = QtGui.QGraphicsLinearLayout()
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
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

        self.__titleItem = NodeTitle(self.__component.getName(), self)
        layout.addItem(self.__titleItem)
        layout.setAlignment(self.__titleItem, QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)

        self.__ports = []
        for i in range(self.__component.getNumInputs()):
            componentInput = component.getInputByIndex(i)
            self.addInputPort(componentInput)

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
        return self.__component.getName()

    def getComponent(self):
        return self.__component

    #########################
    ##

    def addInputPort(self, componentInput):
        port = InputPort(self, self.__graph, componentInput)

        layout = self.layout()
        layout.addItem(port)
        layout.setAlignment(port, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.__ports.append(port)
        self.adjustSize()
        return port

    def addOutputPort(self, componentOutput):
        port = OutputPort(self, self.__graph, componentOutput)

        layout = self.layout()
        layout.addItem(port)
        layout.setAlignment(port, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.__ports.append(port)
        self.adjustSize()
        return port

    def removePort(self, name):
        for i in range(len(self.__ports)):
            port = self.__ports[i]
            if port.getName() == name:
                port.destroy()
                port.deleteLater()
                self.layout().removeItem(port)
                del self.__ports[i]
                self.adjustSize()
        raise Exception("Node: " +  self.getName() + " does not have port:" + name)

    def getPort(self, name):
        for port in self.__ports:
            if port.getName() == name:
                return port
        return None

    def getPortEvalDesc(self, name):
        if self.__evalDesc is not None:
            for portEvalDesc in self.__evalDesc['ports']:
                if portEvalDesc['name'] == name:
                    return portEvalDesc
        return None

    def paint(self, painter, option, widget):
        rect = self.windowFrameRect()
        painter.setBrush(self.__color)
        if self.__selected:
            painter.setPen(self.__selectedPen)
        else:
            painter.setPen(self.__unselectedPen)
        painter.drawRoundRect(rect, 20, 20)

    def isSelected(self):
        return self.__selected

    def setSelected(self, selected):
        self.__selected = selected
        self.update()

    def getGraphPos(self):
        transform = self.transform()
        size = self.size()
        return QtCore.QPointF(transform.dx()+(size.width()*0.5), transform.dy()+(size.height()*0.5))

    def setGraphPos(self, graphPos):
        size = self.size()
        self.setTransform(QtGui.QTransform.fromTranslate(graphPos.x()-(size.width()*0.5), graphPos.y()-(size.height()*0.5)), False)

    def mousePressEvent(self, event):
        if event.button() is QtCore.Qt.MouseButton.LeftButton:
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
        pass
        # if self.__dragging:
        #     if not self.isSelected():
        #         self.__graph.controller().beginInteraction("Move:" + self.getName())
        #         graphPos = self.getGraphPos()
        #         self.__graph.controller().setNodeGraphPos(
        #             nodePath=self.getNodePath(),
        #             graphPos=graphPos
        #         )
        #         self.__graph.controller().endInteraction()
        #     else:
        #         selectedNodes = self.__graph.getSelectedNodes()
        #         names = ""
        #         for node in selectedNodes:
        #             names += (" " + node.getName())
        #         self.__graph.controller().beginInteraction("Move:" + names)
        #         for node in selectedNodes:
        #             graphPos = node.getGraphPos()
        #             self.__graph.controller().setNodeGraphPos(
        #                 nodePath=node.getNodePath(),
        #                 graphPos=graphPos
        #             )
        #         self.__graph.controller().endInteraction()

        #     self.setCursor(QtCore.Qt.ArrowCursor)
        #     self._panning = False
        # else:
        #     super(Node, self).mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        NodeInspectorDockWidget.showWidget(self.__graph.controller(), self.getEvalPath(), self.getNodePath(), floating=True)
        super(Node, self).mouseDoubleClickEvent(event)

    #########################
    ## Events

    def destroy(self):
        # self.__graph.controller().removeNotificationListener('scene.bindingChanged', self.__retrieveBinding)
        # self.__graph.controller().removeNotificationListener('node.posChanged', self.__nodePosChanged)
        # self.__graph.controller().removeNotificationListener('port.created', self.__portAdded)
        # self.__graph.controller().removeNotificationListener('port.destroyed', self.__portRemoved)
        for port in self.__ports:
            port.destroy()
        self.scene().removeItem(self)
