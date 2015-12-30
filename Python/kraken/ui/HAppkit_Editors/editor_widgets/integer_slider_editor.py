from PySide import QtGui, QtCore

from ..fe import FE
from ..widget_factory import EditorFactory

# By importing the Integer_editor here, we ensure that the IntegerEditor is registered
# before the IntegerSliderEditor, meaning the IntegerSliderEditor will take precedence when displaying values with the 'Range' option.
# The registered widgets are checked in reverse order, so that the last registered widgets are checked first.
# this makes it easy to override an existing widget by implimenting a new one and importing the widget you wish to overeride.
import integer_editor
from base_slider_editor import BaseSliderEditor


class IntegerSliderEditor(BaseSliderEditor):

    def __init__(self, valueController, parent=None):

        super(IntegerSliderEditor, self).__init__(valueController, parent=parent)

        hbox = QtGui.QHBoxLayout()

        validator = QtGui.QIntValidator(self)
        validator.setRange(int(self._range['min']), int(self._range['max']))

        self._editEditor.setValidator(validator)
        self._editEditor.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)

        self._sliderEditor.setMinimum(int(self._range['min']))
        self._sliderEditor.setMaximum(int(self._range['max']))
        self._sliderEditor.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)

        self._editEditor.setMinimumWidth(50)
        self._editEditor.setMaximumWidth(90)

        hbox.addWidget(self._editEditor, 1)
        hbox.addWidget(self._sliderEditor, 1)
        hbox.addStretch()
        self.setLayout(hbox)
        self.layout().setContentsMargins(0, 0, 0 ,0)

        self.updateEditorValue()

        if self.isEditable():
            def __sliderPressed():
                self.beginInteraction()

            def __sliderReleased():
                self.endInteraction()

            def __sliderMoved(value):
                if self._updatingEditor:
                    return
                self._editEditor.setText(str(int(value)))
                self._setValueToController(int(value))

            def __textEdited():
                if self._updatingEditor:
                    return
                value = self.getEditorValue()
                # if self._dynamicRange:
                #     self.updateSliderRange(value)

                self._sliderEditor.setValue(value)
                self._setValueToController()

            self._sliderEditor.sliderPressed.connect(__sliderPressed)
            self._sliderEditor.sliderReleased.connect(__sliderReleased)
            self._sliderEditor.valueChanged.connect(__sliderMoved)
            self._editEditor.editingFinished.connect(__textEdited)

    # def updateSliderRange(self, value):
    #     super(IntegerSliderEditor, self).updateSliderRange(value)
    #     self._sliderEditor.setMinimum(self._uiDynamicRange['min'])
    #     self._sliderEditor.setMaximum(self._uiDynamicRange['max'])

    # def keyPressEvent(self, event):
    #     if event.modifiers() == QtCore.Qt.ControlModifier:
    #         super(IntegerSliderEditor, self).keyPressEvent(event)
    #         self._sliderEditor.setMinimum(self._accurateRange['min'])
    #         self._sliderEditor.setMaximum(self._accurateRange['max'])

    # def keyReleaseEvent(self, event):
    #     self._sliderEditor.setMinimum(self._uiDynamicRange['min'])
    #     self._sliderEditor.setMaximum(self._uiDynamicRange['max'])


    def getEditorValue(self):
        return int(self._editEditor.text())


    def setEditorValue(self, value):
        self._editEditor.setText(str(int(value)))
        self._sliderEditor.setValue(value)


    @classmethod
    def canDisplay(cls, valueController):
        return (
                valueController.getDataType() == 'Integer' or
                valueController.getDataType() == 'UInt8' or
                valueController.getDataType() == 'SInt8' or
                valueController.getDataType() == 'UInt16' or
                valueController.getDataType() == 'SInt16' or
                valueController.getDataType() == 'UInt32' or
                valueController.getDataType() == 'SInt32' or
                valueController.getDataType() == 'UInt64' or
                valueController.getDataType() == 'SInt64' or
                valueController.getDataType() == 'Index' or
                valueController.getDataType() == 'Size'
            ) and valueController.hasOption('range')


EditorFactory.registerEditorClass(IntegerSliderEditor)