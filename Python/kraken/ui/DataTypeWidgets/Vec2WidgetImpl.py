from PySide import QtGui, QtCore
from AttributeWidgetImpl import AttributeWidget

class LineEdit(QtGui.QLineEdit):

    def minimumSizeHint(self):
        return QtCore.QSize(10, 25)

    def sizeHint(self):
        return self.minimumSizeHint()

class Vec2Widget(AttributeWidget):

    def __init__(self, attribute, parentWidget=None, addNotificationListener = True):
        super(Vec2Widget, self).__init__(attribute, parentWidget=parentWidget, addNotificationListener = addNotificationListener)

        self.__widgets = []
        hbox = QtGui.QHBoxLayout()

        def defineLineEditSubWidget():
            widget = LineEdit(self)
            validator = QtGui.QDoubleValidator(self)
            validator.setDecimals(3)
            widget.setValidator(validator)
            self.__widgets.append(widget)
            return widget

        self.__editXWidget = defineLineEditSubWidget()
        self.__editYWidget = defineLineEditSubWidget()

        hbox.addWidget(self.__editXWidget, 1)
        hbox.addWidget(self.__editYWidget, 1)
        hbox.addStretch(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)
        self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)

        self.updateWidgetValue()

        if self.isEditable():
            self.__editXWidget.editingFinished.connect(self._invokeSetter)
            self.__editYWidget.editingFinished.connect(self._invokeSetter)
        else:
            self.__editXWidget.setReadOnly(True)
            self.__editYWidget.setReadOnly(True)


    def getWidgetValue(self):
        client = self.getController().getClient()
        scalarKLType = getattr(client.RT.types, 'Scalar')
        vec2KLType = getattr(client.RT.types, 'Vec2')
        return vec2KLType(
            scalarKLType(float(self.__widgets[0].text())),
            scalarKLType(float(self.__widgets[1].text()))
            )
    def setWidgetValue(self, value):
        self.__editXWidget.setText(str(round(value.x, 4)))
        self.__editYWidget.setText(str(round(value.y, 4)))

    @classmethod
    def canDisplay(cls, attribute):
        return attribute.getDataType() == 'Vec2'

Vec2Widget.registerPortWidget()

