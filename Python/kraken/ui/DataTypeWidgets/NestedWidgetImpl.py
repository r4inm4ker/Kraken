import json
from PySide import QtCore, QtGui
from parameter import Parameter
from AttributeWidgetImpl import AttributeWidget

class NestedWidget(AttributeWidget):

    def __init__(self, attribute, parentWidget=None, addNotificationListener = True):

        super(NestedWidget, self).__init__(attribute, parentWidget=parentWidget, addNotificationListener = addNotificationListener)

        self._value = self._invokeGetter()
        self._labels = {}
        self._widgets = {}
        self._gridRow = 0
        self._grid = QtGui.QGridLayout()
        self._grid.setColumnStretch(1, 1)

        if self._attribute.getOption('displayGroupbox', True):
            groupBox = QtGui.QGroupBox(self._attribute.getDataType())
            groupBox.setLayout(self._grid)
            vbox = QtGui.QVBoxLayout()
            vbox.addWidget(groupBox)
            self.setLayout(vbox)
        else:
            self._grid.setContentsMargins(0, 0, 0, 0)
            self.setLayout(self._grid)

    def addValueWidget(self, name, dataType, getter, setter=None):
        port = Parameter(
                controller=self.getController(),
                name=name,
                portType=self._attribute.getPortType(),
                dataType=dataType,
                getterFn=getter,
                setterFn=setter
            )
        widget = AttributeWidget.constructAttributeWidget(self.getController(), port, parentWidget=self, addNotificationListener = False)
        if widget is None:
            return;

        # widget.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        label = QtGui.QLabel(name, self)
        # label.setMaximumWidth(200)
        # label.setContentsMargins(0, 5, 0, 0)
        # label.setMinimumWidth(60)
        # label.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        # label.setAlignment(QtCore.Qt.AlignRight)
        # label.adjustSize()

        rowSpan = widget.getRowSpan()
        columnSpan = widget.getColumnSpan()
        # if columnSpan==1:
        self._grid.addWidget(label, self._gridRow, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        self._grid.addWidget(widget, self._gridRow, 1)#, QtCore.Qt.AlignLeft)
        self._gridRow += 1
        # else:
        #     self._grid.addWidget(label, self._gridRow, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        #     self._grid.addWidget(widget, self._gridRow+1, 0, rowSpan, columnSpan)
        #     self._gridRow += 2

        self._labels[name] = label
        self._widgets[name] = widget

    def addMemberWidget(self, memberName, memberTypeName):
        def memberGetter():
            return getattr(self._value, memberName)
        memberSetter = None
        if self.isEditable():
            def memberSetter(value):
                setattr(self._value, memberName, value)
                self._invokeSetter(self._value)
        self.addValueWidget(memberName, memberTypeName, memberGetter, memberSetter)

    def getWidgetValue(self):
        return self._value

    def setWidgetValue(self, value):
        raise Exception("This method must be implimented by the derived widget:" + self.__class__.__name__)

    def clear(self):
        """
        When the widget is being removed from the inspector,
        this method must be called to unregister the event handlers
        """
        for widget in self._widgets:
            self._widgets[widget].unregisterNotificationListener()
        for label, widget in self._labels.iteritems():
            widget.deleteLater()
        for label, widget in self._widgets.iteritems():
            widget.deleteLater()


    def unregisterNotificationListener(self):
        """
        When the widget is being removed from the inspector,
        this method must be called to unregister the event handlers
        """
        for widget in self._widgets:
            self._widgets[widget].unregisterNotificationListener()
        super(NestedWidget, self).unregisterNotificationListener()

