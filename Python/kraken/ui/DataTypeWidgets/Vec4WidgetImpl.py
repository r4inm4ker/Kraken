from PySide import QtGui, QtCore
from AttributeWidgetImpl import AttributeWidget

class LineEdit(QtGui.QLineEdit):

    def minimumSizeHint(self):
        return QtCore.QSize(10, 25)

    def sizeHint(self):
        return self.minimumSizeHint()

class Vec4Widget(AttributeWidget):

    def __init__(self, attribute, parentWidget=None, addNotificationListener = True):
        super(Vec4Widget, self).__init__(attribute, parentWidget=parentWidget, addNotificationListener = addNotificationListener)

        self.__widgets = []
        hbox = QtGui.QHBoxLayout()

        def defineLineEditSubWidget():
            widget = LineEdit(self)
            validator = QtGui.QDoubleValidator(self)
            validator.setDecimals(2)
            widget.setValidator(validator)
            hbox.addWidget(widget, 1)
            self.__widgets.append(widget)
            return widget


        defineLineEditSubWidget()
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
        vec4KLType = getattr(client.RT.types, 'Vec4')
        return vec4KLType(
            scalarKLType(float(self.__widgets[0].text())),
            scalarKLType(float(self.__widgets[1].text())),
            scalarKLType(float(self.__widgets[2].text())),
            scalarKLType(float(self.__widgets[3].text()))
            )

    def setWidgetValue(self, value):
        self.__widgets[0].setText(str(float(value.x)))
        self.__widgets[1].setText(str(float(value.y)))
        self.__widgets[2].setText(str(float(value.z)))
        self.__widgets[3].setText(str(float(value.t)))

    @classmethod
    def canDisplay(cls, attribute):
        return attribute.getDataType() == 'Vec4'

Vec4Widget.registerPortWidget()