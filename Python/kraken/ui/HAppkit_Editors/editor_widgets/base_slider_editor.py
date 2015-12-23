from PySide import QtGui, QtCore

from ..fe import FE
from ..widget_factory import EditorFactory
from ..base_editor import BaseValueEditor

class BaseSliderEditor(BaseValueEditor):

    def __init__(self, valueController, parent=None):
        super(BaseSliderEditor, self).__init__(valueController, parent=parent)

        self._editEditor = QtGui.QLineEdit(self)
        self._sliderEditor = QtGui.QSlider(QtCore.Qt.Horizontal, self)

        self._range = valueController.getOption('range')
        # self._uiOutOfSliderRange = self._range
        # self._dynamicRange = True
        # self._uiDynamicRange = self._range

        # self._accurateRange = { 'min': 0, 'max': 0 }

        self.setEditable(self.isEditable())


    def setEditable(self, editable):
        self._sliderEditor.setEnabled( editable )
        self._editEditor.setReadOnly( not editable )


    # def updateSliderRange(self, value):
    #     pass
        # offset = None
        # if value < self._uiDynamicRange['min']:
        #     offset = value - self._uiDynamicRange['min']
        # elif value > self._uiDynamicRange['max']:
        #     offset = value - self._uiDynamicRange['max']

        # if offset:
        #     self._uiDynamicRange['min'] += offset
        #     self._uiDynamicRange['max'] += offset
        #     self._valueController.setOption('Range', self._uiDynamicRange)


    # def keyPressEvent(self, event):
    #   modifiers = QtGui.QApplication.keyboardModifiers()
    #   alt = modifiers & QtCore.Qt.AltModifier

    #   factor = None
    #   if alt:
    #     factor = 0.01

    #   if factor is not None:
    #     value = self._invokeGetter()
    #     newRange = (self._uiDynamicRange['max'] - self._uiDynamicRange['min']) * factor
    #     self._accurateRange['min'] = value - newRange * 0.5
    #     self._accurateRange['max'] = value + newRange * 0.5

    #     if self._accurateRange['min'] < self._uiDynamicRange['min']:
    #       self._accurateRange['min'] = self._uiDynamicRange['min']
    #     if self._accurateRange['max'] > self._uiDynamicRange['max']:
    #       self._accurateRange['max'] = self._uiDynamicRange['max']


    # def keyReleaseEvent(self, event):
    #   pass
