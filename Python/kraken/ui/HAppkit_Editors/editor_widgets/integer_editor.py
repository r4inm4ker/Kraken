
import sys
from PySide import QtGui

from ..fe import FE
from ..widget_factory import EditorFactory
from ..base_editor import BaseValueEditor


class IntegerEditor(BaseValueEditor):

    def __init__(self, valueController, parent=None):
        super(IntegerEditor, self).__init__(valueController, parent=parent)
        hbox = QtGui.QHBoxLayout()

        self._editor = QtGui.QSpinBox(self)

        if(self._dataType == 'UInt8' or
            self._dataType == 'UInt16' or
            self._dataType == 'UInt32' or
            self._dataType == 'UInt64' or
            self._dataType == 'Index' or
            self._dataType == 'Size' or
            self._dataType == 'Byte'):
            self._editor.setMinimum(0)
        else:
            self._editor.setMinimum(-100000000)

        self._editor.setMaximum(100000000)
        self._editor.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        hbox.addWidget(self._editor, 1)

        hbox.addStretch(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)

        self.updateEditorValue()

        self._editor.valueChanged.connect(self._setValueToController)

        self.setEditable( valueController.isEditable() )


    def setEditable(self, editable):
        self._editor.setReadOnly( not editable )


    def getEditorValue(self):
        value = self._editor.value()
        return value#self._klType(value)


    def setEditorValue(self, value):
        # Clamp values to avoid OverflowError
        if value > sys.maxint:
            value = sys.maxint
        elif value < -sys.maxint:
            value = -sys.maxint
        self._editor.setValue(value)


    @classmethod
    def canDisplay(cls, valueController):
        dataType = valueController.getDataType()
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


EditorFactory.registerEditorClass(IntegerEditor)
