
#
# Copyright 2010-2014 Fabric Technologies Inc. All rights reserved.
#

#pylint: disable-msg=W0613,R0201
import sys
from PySide import QtGui, QtCore
from DataTypeWidgets import AttributeWidget
from kraken.core.kraken_system import KrakenSystem

from kraken.examples.arm_component import ArmComponentGuide, ArmComponentRig

class ComponentInspector(QtGui.QWidget):
    """A widget providing the ability to nest """

    def __init__(self, component, parent=None):

        # constructors of base classes
        super(ComponentInspector, self).__init__(parent)

        self.parent = parent
        self.component = component

        self.setAttribute(QtCore.Qt.WA_WindowPropagation, True)
        self.setWindowTitle( self.component.getName() + ":" + self.component.getTypeName() )
        self.setWindowFlags( QtCore.Qt.Window )
        self.resize( 300, 300 )

        # layout
        self._mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self._mainLayout)
        self._mainLayout.setContentsMargins(0, 0, 0, 0)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self._paramsFrame = QtGui.QScrollArea(self)
        self._paramsFrame.setWidgetResizable(True)
        self._paramsFrame.setEnabled(True)
        self._paramsFrame.setSizePolicy(sizePolicy)
        self._paramsFrame.setFrameStyle(QtGui.QFrame.StyledPanel)

        self._paramsGroup = QtGui.QWidget(self._paramsFrame)
        self._paramsFrame.setWidget(self._paramsGroup)

        self._paramsLayout = QtGui.QGridLayout()
        self._paramsLayout.setAlignment(QtCore.Qt.AlignTop)
        # self._paramsLayout.setContentsMargins(8, 8, 8, 8)
        # self._paramsLayout.setSpacing(5)

        self._paramsGroup.setLayout(self._paramsLayout)

        self._mainLayout.addWidget(self._paramsFrame)
        self._paramWidgets = []
        self._gridRow = 0

        self.refresh()

    def addValueWidget(self, name, widget):

        label = QtGui.QLabel(name, self._paramsGroup)
        label.setMaximumWidth(200)
        label.setContentsMargins(0, 5, 0, 0)

        if widget is None:
            self._paramsLayout.addWidget(label, self._gridRow, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
            self._gridRow += 1
        else:
            rowSpan = widget.getRowSpan()
            columnSpan = widget.getColumnSpan()
            if columnSpan==1:
                self._paramsLayout.addWidget(label, self._gridRow, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
                self._paramsLayout.addWidget(widget, self._gridRow, 1)
                self._gridRow += 1
            else:
                self._paramsLayout.addWidget(label, self._gridRow, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
                self._paramsLayout.addWidget(widget, self._gridRow+1, 0, rowSpan, columnSpan)
                self._gridRow += 2

            self._paramWidgets.append(widget)
        self.addSeparator()

    def addSeparator(self):
        separatorWidget = QtGui.QFrame(self._paramsGroup)
        separatorWidget.setFrameShape(QtGui.QFrame.HLine)
        self._paramsLayout.addWidget(separatorWidget, self._gridRow, 0, 1, 2)
        self._gridRow += 1

    def addStretch(self, stretch):
        self._paramsLayout.addWidget(QtGui.QWidget(self), self._gridRow, 0, 1, 2)
        self._paramsLayout.setRowStretch(self._gridRow, stretch)
        self._gridRow += 1

    def refresh(self, data=None):
        self.clear()

        def displayAttribute(attribute):
            attributeWidget = AttributeWidget.constructAttributeWidget( attribute, parentWidget=self)
            self.addValueWidget(attribute.getName(), attributeWidget)

        for i in range(self.component.getNumAttributeGroups()):
            grp  = self.component.getAttributeGroupByIndex(i)
            for j in range(grp.getNumAttributes()):
                displayAttribute(grp.getAttributeByIndex(j))

        # Add a stretch so that the widgets pack at the top.
        self.addStretch(2)


    def closeWidget(self, data):
        self.close()

    def clear(self):
        for widget in self._paramWidgets:
            widget.unregisterNotificationListener()
        while self._paramsLayout.count():
            self._paramsLayout.takeAt(0).widget().deleteLater()
        self._paramWidgets = []
        self._gridRow = 0

    ##############################
    ## Events

    def portAdded(self, data):
        self.refresh()

    def portRemoved(self, data):
        self.refresh()

    def onClose(self, event):
        self.clear()
        self.controller.removeNotificationListener('port.added', self.portAdded)
        self.controller.removeNotificationListener('port.removed', self.portRemoved)

        self.controller.removeNotificationListener('scene.new', self.closeWidget)
        self.controller.removeNotificationListener('scene.load', self.closeWidget)



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    armGuide = ArmComponentGuide("arm")

    widget = ComponentInspector(component=armGuide)
    widget.show()
    sys.exit(app.exec_())

