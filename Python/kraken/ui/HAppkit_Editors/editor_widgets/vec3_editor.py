from PySide import QtGui, QtCore

from ..fe import FE
from ..widget_factory import EditorFactory
from ..base_editor import BaseValueEditor


class LineEdit(QtGui.QLineEdit):

    def minimumSizeHint(self):
        return QtCore.QSize(10, 25)

    def sizeHint(self):
        return self.minimumSizeHint()


class Vec3Editor(BaseValueEditor):

    def __init__(self, valueController, parent=None):
        super(Vec3Editor, self).__init__(valueController, parent=parent)

        self.__editors = []
        hbox = QtGui.QHBoxLayout()

        def defineLineEditSubEditor():
            widget = LineEdit(self)
            validator = QtGui.QDoubleValidator(self)
            validator.setDecimals(3)
            widget.setValidator(validator)
            hbox.addWidget(widget, 1)
            self.__editors.append(widget)
            return widget

        defineLineEditSubEditor()
        defineLineEditSubEditor()
        defineLineEditSubEditor()
        hbox.addStretch(0)
        hbox.setContentsMargins(0, 0, 0, 0)

        self.setLayout(hbox)
        self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)

        self.updateEditorValue()

        for i in range(0, len(self.__editors)):
            self.__editors[i].editingFinished.connect(self._setValueToController)

        self.setEditable( valueController.isEditable() )


    def setEditable(self, editable):
        for i in range(0, len(self.__editors)):
            self.__editors[i].setReadOnly( not editable )


    def getEditorValue(self):
        scalarKLType = FE.getInstance().types().Scalar
        vec3KLType = FE.getInstance().types().Vec3
        return vec3KLType(
            scalarKLType(float(self.__editors[0].text())),
            scalarKLType(float(self.__editors[1].text())),
            scalarKLType(float(self.__editors[2].text()))
            )


    def setEditorValue(self, value):
        self.__editors[0].setText(str(round(value.x, 4)))
        self.__editors[1].setText(str(round(value.y, 4)))
        self.__editors[2].setText(str(round(value.z, 4)))


    @classmethod
    def canDisplay(cls, valueController):
        return valueController.getDataType() == 'Vec3'


EditorFactory.registerEditorClass(Vec3Editor)