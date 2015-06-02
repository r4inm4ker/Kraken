
import sys
from PySide import QtGui
from AttributeWidgetImpl import AttributeWidget


class IntegerWidget(AttributeWidget):

    def __init__(self, attribute, parentWidget=None, addNotificationListener = True):
        super(IntegerWidget, self).__init__(attribute, parentWidget=parentWidget, addNotificationListener = addNotificationListener)
        hbox = QtGui.QHBoxLayout()

        self._widget = QtGui.QSpinBox(self)

        if(self._dataType == 'UInt8' or
            self._dataType == 'UInt16' or
            self._dataType == 'UInt32' or
            self._dataType == 'UInt64' or
            self._dataType == 'Index' or
            self._dataType == 'Size' or
            self._dataType == 'Byte'):
            self._widget.setMinimum(0)
        else:
            self._widget.setMinimum(-100000000)
        self._widget.setMaximum(100000000)
        self._widget.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        hbox.addWidget(self._widget, 1)

        hbox.addStretch(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)

        self.updateWidgetValue()

        if self.isEditable():
            self._widget.valueChanged.connect(self._invokeSetter)
        else:
            self._widget.setReadOnly(True)

    def getWidgetValue(self):
        value = self._widget.value()
        return self._klType(value)

    def setWidgetValue(self, value):
        # Clamp values to avoid OverflowError
        if value > sys.maxint:
            value = sys.maxint
        elif value < -sys.maxint:
            value = -sys.maxint
        self._widget.setValue(value)

    @classmethod
    def canDisplay(cls, attribute):
        dataType = attribute.getDataType()
        return (dataType == 'Integer' or
                        dataType == 'UInt8' or
                        dataType == 'SInt8' or
                        dataType == 'UInt16' or
                        dataType == 'SInt16' or
                        dataType == 'UInt32' or
                        dataType == 'SInt32' or
                        dataType == 'UInt64' or
                        dataType == 'SInt64' or
                        dataType == 'Index' or
                        dataType == 'Size' or
                        dataType == 'Byte')

IntegerWidget.registerPortWidget()
