from PySide import QtGui, QtCore

from ..fe import FE
from ..widget_factory import EditorFactory
from ..base_editor import BaseValueEditor

class LineEdit(QtGui.QLineEdit):

    def minimumSizeHint(self):
        return QtCore.QSize(10, 25)

    def sizeHint(self):
        return self.minimumSizeHint()

class Vec4Editor(BaseValueEditor):

    def __init__(self, valueController, parent=None):
        super(Vec4Editor, self).__init__(valueController, parent=parent)

        self.__editors = []
        hbox = QtGui.QHBoxLayout()

        def defineLineEditSubEditor():
            widget = LineEdit(self)
            validator = QtGui.QDoubleValidator(self)
            validator.setDecimals(2)
            widget.setValidator(validator)
            hbox.addWidget(widget, 1)
            self.__editors.append(widget)
            return widget


        defineLineEditSubEditor()
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
        vec4KLType = FE.getInstance().types().Vec4
        return vec4KLType(
            scalarKLType(float(self.__editors[0].text())),
            scalarKLType(float(self.__editors[1].text())),
            scalarKLType(float(self.__editors[2].text())),
            scalarKLType(float(self.__editors[3].text()))
            )


    def setEditorValue(self, value):
        self.__editors[0].setText(str(float(value.x)))
        self.__editors[1].setText(str(float(value.y)))
        self.__editors[2].setText(str(float(value.z)))
        self.__editors[3].setText(str(float(value.t)))


    @classmethod
    def canDisplay(cls, valueController):
        return valueController.getDataType() == 'Vec4'


EditorFactory.registerEditorClass(Vec4Editor)