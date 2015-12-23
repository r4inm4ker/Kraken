from PySide import QtGui, QtCore

from ..fe import FE
from ..widget_factory import EditorFactory

# By importing the ScalarEditor here, we ensure that the ScalarEditor is registered
# before the ScalarSliderEditor, meaning ScalarSliderEditor will take precedence when displaying Scalar values.
# The registered widgets are checked in reverse order, so that the last registered widgets are checked first.
# this makes it easy to override an existing widget by implimenting a new one and importing the widget you wish to overeride.
import scalar_editor
from base_slider_editor import BaseSliderEditor


class ScalarSliderEditor(BaseSliderEditor):
    # Note: all values are multiplied by 1000 on the slider widget, because sliders in
    # Qt are assumed to be integers. This solution isn't the cleanest, but enables a slider to drive scalar values

    def __init__(self, valueController, parent=None):
        super(ScalarSliderEditor, self).__init__(valueController, parent=parent)

        hbox = QtGui.QHBoxLayout()

        validator = QtGui.QDoubleValidator(self)
        validator.setRange(self._range['min'], self._range['max'], 4)

        self._editEditor.setValidator(validator)
        self._editEditor.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)

        self._sliderEditor.setMinimum(self._range['min'] * 1000)
        self._sliderEditor.setMaximum(self._range['max'] * 1000)
        self._sliderEditor.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        self._sliderEditor.setTickInterval(1000)

        self._editEditor.setMinimumWidth(50)
        self._editEditor.setMaximumWidth(90)

        hbox.addWidget(self._editEditor, 1)
        hbox.addWidget(self._sliderEditor, 1)
        hbox.addStretch()
        self.setLayout(hbox)
        self.layout().setContentsMargins(0, 0, 0 ,0)

        self.updateEditorValue()

        def __sliderPressed():
            self.beginInteraction()

        def __sliderReleased():
            self.endInteraction()

        def __sliderMoved(value):
            if self._updatingEditor:
                return
            value = float(value) / 1000
            self._editEditor.setText(str(round(value, 4)))
            self._value = value
            self._setValueToController()

        def __textEdited():
            if self._updatingEditor:
                return
            value = self.getEditorValue()
            # if self._dynamicRange:
            #     self.updateSliderRange(value)
            self._sliderEditor.setValue(value * 1000)
            self._setValueToController()

        self._sliderEditor.sliderPressed.connect(__sliderPressed)
        self._sliderEditor.sliderReleased.connect(__sliderReleased)
        self._sliderEditor.valueChanged.connect(__sliderMoved)
        self._editEditor.editingFinished.connect(__textEdited)

        self.setEditable( valueController.isEditable() )


    def setEditable(self, editable):
        self._editEditor.setReadOnly( not editable )
        self._sliderEditor.setEnabled( editable )

    def getEditorValue(self):
        return float(self._editEditor.text())


    def setEditorValue(self, value):
        self._updatingEditor = True
        self._editEditor.setText(str(round(value, 4)))
        self._sliderEditor.setValue(value * 1000)
        self._updatingEditor = False


    # def updateSliderRange(self, value):
    #     super(ScalarSliderEditor, self).updateSliderRange(value)
    #     self._sliderEditor.setMinimum(self._uiDynamicRange['min'] * 1000)
    #     self._sliderEditor.setMaximum(self._uiDynamicRange['max'] * 1000)


    # def keyPressEvent(self, event):
    #     if event.modifiers() == QtCore.Qt.ControlModifier:
    #         super(ScalarSliderEditor, self).keyPressEvent(event)
    #         self._sliderEditor.setMinimum(self._accurateRange['min'] * 1000)
    #         self._sliderEditor.setMaximum(self._accurateRange['max'] * 1000)


    # def keyReleaseEvent(self, event):
    #     self._sliderEditor.setMinimum(self._uiDynamicRange['min'] * 1000)
    #     self._sliderEditor.setMaximum(self._uiDynamicRange['max'] * 1000)


    @classmethod
    def canDisplay(cls, valueController):
        return (
                valueController.getDataType() == 'Scalar' or
                valueController.getDataType() == 'Float32' or
                valueController.getDataType() == 'Float64'
            ) and valueController.hasOption('range')


EditorFactory.registerEditorClass(ScalarSliderEditor)