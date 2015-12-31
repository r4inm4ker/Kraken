from PySide import QtGui, QtCore

from ..fe import FE
from ..widget_factory import EditorFactory
from ..base_editor import BaseValueEditor


class LineEditEditor(QtGui.QLineEdit):
    def __init__(self, valueController, parent=None):
        super(LineEditEditor, self).__init__(parent)
        self._valueController = valueController


    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            self._valueController.setValue(event.mimeData().text())
            event.acceptProposedAction()


class LineEditor(BaseValueEditor):

    def __init__(self, valueController, parent=None):
        super(LineEditor, self).__init__(valueController, parent=parent)

        hbox = QtGui.QHBoxLayout()

        self._editor = LineEditEditor(valueController, parent=self)
        hbox.addWidget(self._editor, 1)

        hbox.addStretch(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)

        self.updateEditorValue()

        # we get lots of 'editingFinished' events,
        # so filter to only generate undos for important ones.
        self._value = valueController.getValue()
        def invokeSetter():
            value = self._editor.text()
            if self._value != value:
                self._value = value
                self._setValueToController()
        self._editor.editingFinished.connect(invokeSetter)

        self.setEditable( valueController.isEditable() )


    def setEditable(self, editable):
        self._editor.setReadOnly( not editable )
        self.setAcceptDrops(editable)


    def getEditorValue(self):
        return self._editor.text()


    def setEditorValue(self, value):
        self._editor.setText(value)


    @classmethod
    def canDisplay(cls, valueController):
        if valueController.getDataType() == 'String':
            value = valueController.getValue()
            if value.find('\n') > -1:
                return False
            return True
        return False


EditorFactory.registerEditorClass(LineEditor)
