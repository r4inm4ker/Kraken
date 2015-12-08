from PySide import QtGui, QtCore
from AttributeWidgetImpl import AttributeWidget


# By importing the ComboBoxWidget here, we ensure that the ComboBoxWidget is registered
# before the ListViewWidget, meaning the ListViewWidget will take precedence when displaying values with the 'Combo' option.
# The registered widgets are checked in reverse order, so that the last registered widgets are checked first.
# this makes it easy to override an existing widget by implimenting a new one and importing the widget you wish to overeride.
import ComboBoxWidgetImpl

class ListViewWidget(AttributeWidget):

    def __init__(self, attribute, parentWidget=None, addNotificationListener = True):
        super(ListViewWidget, self).__init__(attribute, parentWidget=parentWidget, addNotificationListener = addNotificationListener)


        hbox = QtGui.QHBoxLayout()
        self._widget = QtGui.QListWidget(self)

        self.__items = attribute.getOption('Combo')
        for item in self.__items:
            self._widget.addItem(str(item))
        self._widget.setMaximumHeight(65)

        hbox.addWidget(self._widget, 1)

        hbox.addStretch(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)

        self.updateWidgetValue()

        if self.isEditable():
            self._widget.itemSelectionChanged.connect(self._invokeSetter)
        else:
            self._widget.setReadOnly(True)

    def getWidgetValue(self):
        return self.__items[self._widget.currentRow()]

    def setWidgetValue(self, value):
        self._updatingWidget = True
        if value in self.__items:
            index = self.__items.index(value)
        else:
            index = 0
        self._widget.setCurrentItem(self._widget.item(index))
        self._updatingWidget = False

    @classmethod
    def canDisplay(cls, attribute):
        return attribute.getDataType() == 'String' and attribute.hasOption('Combo')


ListViewWidget.registerPortWidget()


