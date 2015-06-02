from PySide import QtGui


class AttributeWidget(QtGui.QWidget):

    __registeredWidgets = []

    def __init__(self, attribute, parentWidget=None, addNotificationListener = True):
        super(AttributeWidget, self).__init__(parentWidget)

        # self.setMinimumWidth(AttributeWidget.getPortWidgetMinWidth())
        # self.setMaximumWidth(AttributeWidget.getPortWidgetMaxWidth())
        # self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        # self.setContentsMargins(4, 4, 4, 4)

        self._attribute = attribute
        self._dataType = attribute.getDataType()

        self._updatingWidget = False
        self._firingSetter = False
        self.__interactionInProgress = False

        # self.__notificationListenerAdded = False
        # if addNotificationListener:
        #     self._attribute.addNotificationListener('value.changed', self._onValueChange)
        #     self.__notificationListenerAdded = True

    def getAttribute(self):
        return self._attribute

    def isEditable(self):
        return True

    def getName(self):
        return self._attribute.getName()

    def getLabel(self):
        return self._attribute.getName()

    def updateWidgetValue(self):
        self.setWidgetValue(self._invokeGetter())

    def setWidgetValue(self, value):
        """This method is used to update the value displayed by the widget. Must be defined in a derived class"""
        raise Exception("setWidgetValue not implimented: "+self.__name)

    def getWidgetValue(self):
        """This method is used to return the value displayed in the widget. Must be defined in a derived class"""
        raise Exception("getWidgetValue not implimented: "+self.__name)

    def _invokeGetter(self):
        return self._attribute.getValue()

    def _onValueChange(self, data):
        """This method is fired when the port has changed and the widget needs to be updated to display the new value"""

        # TODO: some widgets may want to override the updated value, but this behavior makes editing string widgets really annoying
        # as it re-focusses the widget after every change. I made '_onValueChange' protected so that derived widgets can override it.
        if not self.__interactionInProgress:
            self._updatingWidget = True
            self.setWidgetValue(data['value'])
            self._updatingWidget = False

    def beginInteraction(self):
        # self._controller.beginUndoBracket(name=self._attribute.getName() + " changed")
        self.__interactionInProgress = True

    def endInteraction(self):
        self.__interactionInProgress = False
        # self._controller.endUndoBracket()

    def _invokeSetter(self, value = None):
        if self._updatingWidget:
            return
        interactionInProgress = self.__interactionInProgress
        if not interactionInProgress:
            self.beginInteraction()

        self._firingSetter  = True
        # some value changes, such as resizing arrays, requires that the widget be re-built.
        # in those cases, we should provide the value to the setter.
        # if value is None:
        # For now this is disabled, because we always want to set an RTVal on the attribute.
        # (getWidgetValue should now always return an RTVal)
        value = self.getWidgetValue()

        self._attribute.setValue(value)
        self._firingSetter  = False

        if not interactionInProgress:
            self.endInteraction()

    # def unregisterNotificationListener(self):
    #     """When the widget is being removed fromthe inspector, this method must be called to unregister the event handlers"""
    #     if self.__notificationListenerAdded:
    #         self._attribute.removeNotificationListener('value.changed', self._onValueChange)
    #         self.__notificationListenerAdded = False

    def getMinLabelWidth(self):
        return self._minLabelWidth

    def setMinLabelWidth(self, value):
        self._minLabelWidth = value

    def getRowSpan(self):
        """Returns the number of rows in the layout grid this widget takes up."""
        return 1

    def getColumnSpan(self):
        """Returns the number of columns in the layout grid this widget takes up. Wide widgets can return values greater than 1 to modify thier alignment relative to the label."""
        return 1

    @classmethod
    def canDisplay(cls, attribute):
        """Must be overridden for every subclasses"""
        raise Exception("Class method 'canDisplay()' must be implemented in widget: " + str(cls))

    @staticmethod
    def getPortWidgetMinWidth():
        return 60

    @staticmethod
    def getPortWidgetMaxWidth():
        return 1024

    @classmethod
    def registerPortWidget(cls):
        cls.__registeredWidgets.append(cls)

    @classmethod
    def constructAttributeWidget(cls, attribute, parentWidget=None, addNotificationListener = True):
        if attribute is None:
            raise Exception("attribute is None")
        for widgetCls in reversed(cls.__registeredWidgets):
            if widgetCls.canDisplay(attribute):
                return widgetCls(attribute, parentWidget=parentWidget, addNotificationListener = addNotificationListener)
        return None
