from PySide import QtGui, QtCore

from BaseSliderWidgetImpl import BaseSliderWidget

# By importing the ScalarWidget here, we ensure that the ScalarWidget is registered
# before the ScalarSliderWidget, meaning ScalarSliderWidget will take precedence when displaying Scalar values.
# The registered widgets are checked in reverse order, so that the last registered widgets are checked first.
# this makes it easy to override an existing widget by implimenting a new one and importing the widget you wish to overeride.
import ScalarWidgetImpl


class ScalarSliderWidget(BaseSliderWidget):
    # Note: all values are multiplied by 1000 on the slider widget, because sliders in
    # Qt are assumed to be integers. This solution isn't the cleanest, but enables a slider to drive scalar values

    def __init__(self, attribute, parentWidget=None, addNotificationListener = True):
        super(ScalarSliderWidget, self).__init__(attribute, parentWidget=parentWidget, addNotificationListener = addNotificationListener)

        hbox = QtGui.QHBoxLayout()

        validator = QtGui.QDoubleValidator(self)
        if not self._dynamicRange:
            validator.setRange(self._uiOutOfSliderRange['min'], self._uiOutOfSliderRange['max'], 4)
        self._editWidget.setValidator(validator)
        self._editWidget.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)

        self._sliderWidget.setMinimum(self._range['min'] * 1000)
        self._sliderWidget.setMaximum(self._range['max'] * 1000)
        self._sliderWidget.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        self._sliderWidget.setTickInterval(1000)

        self._editWidget.setMinimumWidth(50)
        self._editWidget.setMaximumWidth(90)

        hbox.addWidget(self._editWidget, 1)
        hbox.addWidget(self._sliderWidget, 1)
        hbox.addStretch()
        self.setLayout(hbox)
        self.layout().setContentsMargins(0, 0, 0 ,0)

        self.updateWidgetValue()

        if self.isEditable():
            def __sliderPressed():
                self.beginInteraction()

            def __sliderReleased():
                self.endInteraction()

            def __sliderMoved(value):
                if self._updatingWidget:
                    return
                value = float(value) / 1000
                self._editWidget.setText(str(round(value, 4)))
                self._value = value
                self._invokeSetter()

            def __textEdited():
                if self._updatingWidget:
                    return
                value = self.getWidgetValue()
                if self._dynamicRange:
                    self.updateSliderRange(value)
                self._sliderWidget.setValue(value * 1000)
                self._invokeSetter()

            self._sliderWidget.sliderPressed.connect(__sliderPressed)
            self._sliderWidget.sliderReleased.connect(__sliderReleased)
            self._sliderWidget.valueChanged.connect(__sliderMoved)
            self._editWidget.editingFinished.connect(__textEdited)


    def updateSliderRange(self, value):
        super(ScalarSliderWidget, self).updateSliderRange(value)
        self._sliderWidget.setMinimum(self._uiDynamicRange['min'] * 1000)
        self._sliderWidget.setMaximum(self._uiDynamicRange['max'] * 1000)

    def keyPressEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier:
            super(ScalarSliderWidget, self).keyPressEvent(event)
            self._sliderWidget.setMinimum(self._accurateRange['min'] * 1000)
            self._sliderWidget.setMaximum(self._accurateRange['max'] * 1000)

    def keyReleaseEvent(self, event):
        self._sliderWidget.setMinimum(self._uiDynamicRange['min'] * 1000)
        self._sliderWidget.setMaximum(self._uiDynamicRange['max'] * 1000)

    def getWidgetValue(self):
        return float(self._editWidget.text())

    def setWidgetValue(self, value):
        self._updatingWidget = True
        self._editWidget.setText(str(round(value, 4)))
        self._sliderWidget.setValue(value * 1000)
        self._updatingWidget = False

    @classmethod
    def canDisplay(cls, attribute):
        return (
                attribute.getDataType() == 'Scalar' or
                attribute.getDataType() == 'Float32' or
                attribute.getDataType() == 'Float64'
            ) and ( attribute.getMin() < attribute.getMax() )


ScalarSliderWidget.registerPortWidget()