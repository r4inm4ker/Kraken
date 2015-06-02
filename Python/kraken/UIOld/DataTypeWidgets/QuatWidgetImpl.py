from PySide import QtGui, QtCore
from AttributeWidgetImpl import AttributeWidget
import math


class LineEdit(QtGui.QLineEdit):

    def minimumSizeHint(self):
        return QtCore.QSize(10, 25)

    def sizeHint(self):
        return self.minimumSizeHint()

class QuatWidget(AttributeWidget):

    def __init__(self, attribute, parentWidget=None, addNotificationListener = True):
        super(QuatWidget, self).__init__(attribute, parentWidget=parentWidget, addNotificationListener = addNotificationListener)

        self.__widgets = []
        hbox = QtGui.QHBoxLayout()

        def defineLineEditSubWidget():
            widget = LineEdit(self)
            validator = QtGui.QDoubleValidator(self)
            validator.setDecimals(3)
            widget.setValidator(validator)
            hbox.addWidget(widget, 1)
            self.__widgets.append(widget)

            return widget

        defineLineEditSubWidget()
        defineLineEditSubWidget()
        defineLineEditSubWidget()
        hbox.addStretch(0)
        hbox.setContentsMargins(0, 0, 0, 0)

        self.setLayout(hbox)
        self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)

        self.updateWidgetValue()
        if self.isEditable():
            for i in range(0, len(self.__widgets)):
                self.__widgets[i].editingFinished.connect(self._invokeSetter)
        else:
            for i in range(0, len(self.__widgets)):
                self.__widgets[i].setReadOnly(True)

    def getWidgetValue(self):
        client = self.getController().getClient()
        scalarKLType = getattr(client.RT.types, 'Scalar')
        quatKLType = getattr(client.RT.types, 'Quat')
        eulerKLType = getattr(client.RT.types, 'Euler')
        return quatKLType(
            eulerKLType(
                scalarKLType(float(self.__widgets[0].text())),
                scalarKLType(float(self.__widgets[1].text())),
                scalarKLType(float(self.__widgets[2].text()))
            ))

    def setWidgetValue(self, value):
        euler = value.toEulerAngles("Euler")
        self.__widgets[0].setText(str(round(math.degrees(euler.x), 4)))
        self.__widgets[1].setText(str(round(math.degrees(euler.y), 4)))
        self.__widgets[2].setText(str(round(math.degrees(euler.z), 4)))

    @classmethod
    def canDisplay(cls, attribute):
        return False
        # return attribute.getDataType() == 'Quat'

QuatWidget.registerPortWidget()