from PySide import QtGui, QtCore
from BaseSliderWidgetImpl import BaseSliderWidget

# By importing the IntegerWidgetImpl here, we ensure that the IntegerWidgetImpl is registered
# before the IntegerSliderWidget, meaning the IntegerSliderWidget will take precedence when displaying values with the 'Range' option.
# The registered widgets are checked in reverse order, so that the last registered widgets are checked first.
# this makes it easy to override an existing widget by implimenting a new one and importing the widget you wish to overeride.
import IntegerWidgetImpl


class IntegerSliderWidget(BaseSliderWidget):

    def __init__(self, attribute, parentWidget=None, addNotificationListener = True):

        super(IntegerSliderWidget, self).__init__(attribute, parentWidget=parentWidget, addNotificationListener = addNotificationListener)

        hbox = QtGui.QHBoxLayout()

        validator = QtGui.QIntValidator(self)
        if not self._dynamicRange:
            validator.setRange(int(self._uiOutOfSliderRange['min']), int(self._uiOutOfSliderRange['max']))
        self._editWidget.setValidator(validator)
        self._editWidget.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)

        self._sliderWidget.setMinimum(int(self._range['min']))
        self._sliderWidget.setMaximum(int(self._range['max']))
        self._sliderWidget.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)

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
                self._editWidget.setText(str(int(value)))
                self._invokeSetter(int(value))

            def __textEdited():
                if self._updatingWidget:
                    return
                value = self.getWidgetValue()
                if self._dynamicRange:
                    self.updateSliderRange(value)

                self._sliderWidget.setValue(value)
                self._invokeSetter()

            self._sliderWidget.sliderPressed.connect(__sliderPressed)
            self._sliderWidget.sliderReleased.connect(__sliderReleased)
            self._sliderWidget.valueChanged.connect(__sliderMoved)
            self._editWidget.editingFinished.connect(__textEdited)

    def updateSliderRange(self, value):
        super(IntegerSliderWidget, self).updateSliderRange(value)
        self._sliderWidget.setMinimum(self._uiDynamicRange['min'])
        self._sliderWidget.setMaximum(self._uiDynamicRange['max'])

    def keyPressEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier:
            super(IntegerSliderWidget, self).keyPressEvent(event)
            self._sliderWidget.setMinimum(self._accurateRange['min'])
            self._sliderWidget.setMaximum(self._accurateRange['max'])

    def keyReleaseEvent(self, event):
        self._sliderWidget.setMinimum(self._uiDynamicRange['min'])
        self._sliderWidget.setMaximum(self._uiDynamicRange['max'])

    def getWidgetValue(self):
        return int(self._editWidget.text())


    def setWidgetValue(self, value):
        self._editWidget.setText(str(int(value)))
        self._sliderWidget.setValue(value)

    @classmethod
    def canDisplay(cls, attribute):
        return  (
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
                ) and ( attribute.getMin() < attribute.getMax() )


IntegerSliderWidget.registerPortWidget()