
#
# Copyright 2010-2014 Fabric Technologies Inc. All rights reserved.
#

#pylint: disable-msg=W0613,R0201
import sys
from PySide import QtGui, QtCore
from DataTypeWidgets import AttributeWidget
from kraken.core.kraken_system import KrakenSystem



class _NameAttributeProxy(object):

    def __init__(self, component, nodeItem):
        super(_NameAttributeProxy, self).__init__()
        self.component = component
        self.nodeItem = nodeItem

    def setValue(self, value):
        # Store original node name
        origName = self.nodeItem.getName()
        self.component.setName(value)
        if origName != self.component.getDecoratedName():
            self.nodeItem.nameChanged(origName)

    def getValue(self):
        return self.component.getName()

    def getDataType(self):
        return 'String'

class _LocationAttributeProxy(object):

    def __init__(self, component, nodeItem):
        super(_LocationAttributeProxy, self).__init__()
        self.component = component
        self.nodeItem = nodeItem

    def setValue(self, value):
        # Store original node name
        origName = self.nodeItem.getName()
        self.component.setLocation(value)
        if origName != self.component.getDecoratedName():
            self.nodeItem.nameChanged(origName)

    def getValue(self):
        return self.component.getLocation()

    def getDataType(self):
        return 'String'

class ComponentInspector(QtGui.QWidget):
    """A widget providing the ability to nest """

    def __init__(self, component, parent=None, nodeItem=None):

        # constructors of base classes
        super(ComponentInspector, self).__init__(parent)
        self.setObjectName('componentInspector')

        self.parent = parent
        self.component = component
        self.nodeItem = nodeItem

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

        self._paramsGroup.setLayout(self._paramsLayout)

        self._mainLayout.addWidget(self._paramsFrame)
        self._paramWidgets = []
        self._gridRow = 0

        self.refresh()

    def addAttrWidget(self, name, widget):

        label = QtGui.QLabel(name, self._paramsGroup)
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

    def addSeparator(self, name=None):

        separatorWidget = QtGui.QFrame(self._paramsGroup)
        separatorWidget.setFrameShape(QtGui.QFrame.HLine)
        separatorWidget.setObjectName('separatorFrame')
        if name is not None:
            labelWidget = QtGui.QLabel(name, self._paramsGroup)
            labelWidget.setObjectName('separatorLabel')
            labelWidget.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
            self._paramsLayout.addWidget(labelWidget, self._gridRow, 0)
            self._paramsLayout.addWidget(separatorWidget, self._gridRow, 1, QtCore.Qt.AlignBottom)
            self._gridRow += 1
        else:
            self._paramsLayout.addWidget(separatorWidget, self._gridRow, 0, 1, 2)
            self._gridRow += 1


    def addStretch(self, stretch):
        self._paramsLayout.addWidget(QtGui.QWidget(self), self._gridRow, 0, 1, 2)
        self._paramsLayout.setRowStretch(self._gridRow, stretch)
        self._gridRow += 1

    def refresh(self, data=None):
        self.clear()

        nameAttributeProxy = _NameAttributeProxy(component=self.component, nodeItem=self.nodeItem)
        nameWidget = AttributeWidget.constructAttributeWidget( nameAttributeProxy, parentWidget=self)
        self.addAttrWidget("name", nameWidget)

        locationAttributeProxy = _LocationAttributeProxy(component=self.component, nodeItem=self.nodeItem)
        locationWidget = AttributeWidget.constructAttributeWidget( locationAttributeProxy, parentWidget=self)
        self.addAttrWidget("location", locationWidget)


        def displayAttribute(attribute):
            attributeWidget = AttributeWidget.constructAttributeWidget( attribute, parentWidget=self)
            self.addAttrWidget(attribute.getName(), attributeWidget)

        for i in range(self.component.getNumAttributeGroups()):
            grp  = self.component.getAttributeGroupByIndex(i)
            self.addSeparator(grp.getName())
            for j in range(grp.getNumAttributes()):
                displayAttribute(grp.getAttributeByIndex(j))

        # Add a stretch so that the widgets pack at the top.
        self.addStretch(2)


    def closeWidget(self, data):
        self.close()

    def clear(self):
        # for widget in self._paramWidgets:
        #     widget.unregisterNotificationListener()
        while self._paramsLayout.count():
            self._paramsLayout.takeAt(0).widget().deleteLater()
        self._paramWidgets = []
        self._gridRow = 0


    ##############################
    ## Events

    def closeEvent(self, event):
        if self.nodeItem is not None:
            self.nodeItem.inspectorClosed()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    from kraken_examples.arm_component import ArmComponentGuide, ArmComponentRig
    armGuide = ArmComponentGuide("arm")

    widget = ComponentInspector(component=armGuide)
    widget.show()
    sys.exit(app.exec_())

