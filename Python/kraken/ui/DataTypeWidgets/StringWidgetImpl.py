from PySide import QtGui, QtCore
from AttributeWidgetImpl import AttributeWidget


class StringWidget(AttributeWidget):

    def __init__(self, attribute, parentWidget=None, addNotificationListener = True):
        super(StringWidget, self).__init__(attribute, parentWidget=parentWidget, addNotificationListener = addNotificationListener)

        vbox = QtGui.QVBoxLayout()

        self._widget = QtGui.QTextEdit(self)
        options = attribute.getOption('Multiline')
        self._widget.setMinimumHeight(20)
        self._widget.setMaximumHeight( options.get('numLines', 5) * 20 )
        vbox.addWidget(self._widget, 1)

        # vbox.addStretch(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vbox)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)

        self.updateWidgetValue()

        if self.isEditable():
            # we get lots of 'editingFinished' events,
            # so filter to only generate undos for important ones.

            client = self.getController().getClient()
            self._value = self._widget.toPlainText()
            def invokeSetter():
                value = self._widget.toPlainText()
                if self._value != value:
                    self._value = value
                    self._invokeSetter()
            self._widget.textChanged.connect(self._invokeSetter)
        else:
            self._widget.setReadOnly(True)


    def getWidgetValue(self):
        return self._widget.toPlainText()

    def setWidgetValue(self, value):
        self._widget.setText(value)

    def getColumnSpan(self):
        """Returns the number of columns in the layout grid this widget takes up. Wide widgets can return values greater than 1 to modify thier alignment relative to the label."""
        return 2

    @classmethod
    def canDisplay(cls, attribute):
        # if attribute.getDataType() == 'String':
        #     if attribute.hasOption('Multiline'):
        #         return True
        #     else:
        #         value = attribute.getValue()
        #         if value.find('\n') > -1:
        #             return True
        return False



StringWidget.registerPortWidget()

