
#
# Copyright 2010-2015
#


import json
from PySide import QtGui, QtCore

from pyflowgraph.node import Node
from pyflowgraph.port import PortCircle, BasePort, PortLabel

from kraken.core.maths import Vec2

from kraken.ui.component_inspector import ComponentInspector


class KBackdrop(Node):

    def __init__(self, graph):
        super(KBackdrop, self).__init__(graph, 'backdrop')

        self.__inspectorWidget = None

        # self.setGraphPos( QtCore.QPointF( self.__component.getGraphPos().x, self.__component.getGraphPos().y ) )
        self.setColor(QtGui.QColor(65, 120, 122, 255))

    #########################
    ## Events

    def mouseDoubleClickEvent(self, event):
        # if self.__inspectorWidget is None:
        #     parentWidget = self.getGraph().getGraphViewWidget()
        #     self.__inspectorWidget = ComponentInspector(component=self.__component, parent=parentWidget, nodeItem=self)
        #     self.__inspectorWidget.show()
        # else:
        #     self.__inspectorWidget.setFocus()

        super(KBackdrop, self).mouseDoubleClickEvent(event)


    def inspectorClosed(self):
        self.__inspectorWidget = None


