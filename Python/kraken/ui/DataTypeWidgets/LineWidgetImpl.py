from PySide import QtGui, QtCore
from AttributeWidgetImpl import AttributeWidget


class LineWidget(AttributeWidget):

    def __init__(self, attribute, parentWidget=None, addNotificationListener = True):
        super(LineWidget, self).__init__(attribute, parentWidget=parentWidget, addNotificationListener = addNotificationListener)

        hbox = QtGui.QHBoxLayout()

        self._widget = QtGui.QLineEdit(self)
        hbox.addWidget(self._widget, 1)

        hbox.addStretch(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)

        self.updateWidgetValue()
        if self.isEditable():
            # we get lots of 'editingFinished' events,
            # so filter to only generate undos for important ones.
            self._value = attribute.getValue()
            def invokeSetter():
                value = self._widget.text()
                if self._value != value:
                    self._value = value
                    self._invokeSetter()
            self._widget.editingFinished.connect(invokeSetter)
        else:
            self._widget.setReadOnly(True)

    def getWidgetValue(self):
        return self._widget.text()

    def setWidgetValue(self, value):
        self._widget.setText(value)

    @classmethod
    def canDisplay(cls, attribute):
        if attribute.getDataType() == 'String':
            value = attribute.getValue()
            if value.find('\n') > -1:
                return False
            return True
        return False


LineWidget.registerPortWidget()

