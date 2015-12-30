from PySide import QtGui, QtCore

from ..fe import FE
from ..widget_factory import EditorFactory
from ..base_editor import BaseValueEditor

class LineEdit(QtGui.QLineEdit):

    def minimumSizeHint(self):
        return QtCore.QSize(10, 25)

    def sizeHint(self):
        return self.minimumSizeHint()

class Vec2Editor(BaseValueEditor):

    def __init__(self, valueController, parent=None):
        super(Vec2Editor, self).__init__(valueController, parent=parent)

        self.__editors = []
        hbox = QtGui.QHBoxLayout()

        def defineLineEditSubEditor():
            widget = LineEdit(self)
            validator = QtGui.QDoubleValidator(self)
            validator.setDecimals(3)
            widget.setValidator(validator)
            self.__editors.append(widget)
            return widget

        self.__editXEditor = defineLineEditSubEditor()
        self.__editYEditor = defineLineEditSubEditor()

        hbox.addWidget(self.__editXEditor, 1)
        hbox.addWidget(self.__editYEditor, 1)
        hbox.addStretch(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)
        self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)

        self.updateEditorValue()

        self.__editXEditor.editingFinished.connect(self._setValueToController)
        self.__editYEditor.editingFinished.connect(self._setValueToController)

        self.setEditable( valueController.isEditable() )


    def setEditable(self, editable):
        self.__editXEditor.setReadOnly( not editable )
        self.__editYEditor.setReadOnly( not editable )


    def getEditorValue(self):
        scalarKLType = FE.getInstance().types().Scalar
        vec2KLType = FE.getInstance().types().Vec2
        return vec2KLType(
            scalarKLType(float(self.__editors[0].text())),
            scalarKLType(float(self.__editors[1].text()))
            )


    def setEditorValue(self, value):
        self.__editXEditor.setText(str(round(value.x, 4)))
        self.__editYEditor.setText(str(round(value.y, 4)))


    @classmethod
    def canDisplay(cls, valueController):
        return valueController.getDataType() == 'Vec2'


EditorFactory.registerEditorClass(Vec2Editor)
