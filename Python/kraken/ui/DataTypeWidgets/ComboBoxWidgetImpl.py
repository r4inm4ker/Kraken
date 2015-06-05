from PySide import QtGui, QtCore
from AttributeWidgetImpl import AttributeWidget


class ComboBoxWidget(AttributeWidget):

    def __init__(self, attribute, parentWidget=None, addNotificationListener = True):
        super(ComboBoxWidget, self).__init__(attribute, parentWidget=parentWidget, addNotificationListener = addNotificationListener)


        self.__name = attribute.getName()
        self._items = []

        hbox = QtGui.QHBoxLayout()

        self._widget = QtGui.QComboBox(self)
        hbox.addWidget(self._widget, 1)

        hbox.addStretch(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)

        items = attribute.getOption('Combo')
        if items is not None:
            self.setComboBoxItems(items)
            self.updateWidgetValue()

        if self.isEditable():
            self._widget.currentIndexChanged.connect(self._setValue)
        else:
            self._widget.setEnabled(False)


    def _setValue(self):
        # In the case of a combo box with no items, we still get 'currentIndexChanged' events,
        # but must filter tem out here. We also don't want to propagate changes back to the
        # scene when updating the combo box items.
        if len(self._items) == 0 or self._updatingWidget:
            return
        self._invokeSetter()

    def setComboBoxItems(self, items):
        self._updatingWidget = True
        # Store the previous item, so we can maintain the selection after updating.
        currentItem = None
        if self._items is not None and self._widget.currentIndex() >= 0 and self._widget.currentIndex() < len(self._items):
            currentItem = self._items[self._widget.currentIndex()]
        self._widget.clear()
        index = 0
        for item in items:
            self._widget.addItem(item)
            if item == currentItem:
                # restore the previous selection
                self._widget.setCurrentIndex(int(value))
            index = index + 1
        self._items = items
        self.setStyleSheet("QComboBox QAbstractItemView  { min-height: " + str(len(self._items)) + "px; }")
        self._updatingWidget = False


    def getWidgetValue(self):
        return self._klType(self._widget.currentIndex())

    def setWidgetValue(self, value):
        self._updatingWidget = True
        self._widget.setCurrentIndex(int(value))
        self._updatingWidget = False


    def unregisterNotificationListener(self):
        """
        When the widget is being removed from the inspector,
        this method must be called to unregister the event handlers
        """
        super(ComboBoxWidget, self).unregisterNotificationListener()

    @classmethod
    def canDisplay(cls, attribute):
        return attribute.hasOption('Combo') and (
                    attribute.getDataType() == 'Integer' or
                    attribute.getDataType() == 'UInt8' or
                    attribute.getDataType() == 'SInt8' or
                    attribute.getDataType() == 'UInt16' or
                    attribute.getDataType() == 'SInt16' or
                    attribute.getDataType() == 'UInt32' or
                    attribute.getDataType() == 'SInt32' or
                    attribute.getDataType() == 'UInt64' or
                    attribute.getDataType() == 'SInt64' or
                    attribute.getDataType() == 'Index' or
                    attribute.getDataType() == 'Size'
                )

ComboBoxWidget.registerPortWidget()
