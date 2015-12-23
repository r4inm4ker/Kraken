from PySide import QtGui, QtCore

from ..fe import FE
from ..widget_factory import EditorFactory
from ..base_editor import BaseValueEditor


class StringEditor(BaseValueEditor):

    def __init__(self, valueController, parent=None):
        super(StringEditor, self).__init__(valueController, parent=parent)

        vbox = QtGui.QVBoxLayout()

        self._editor = QtGui.QTextEdit(self)
        options = valueController.getOption('multiLine')
        self._editor.setMinimumHeight( options.get('numLines', 5) * 20 )
        self._editor.setMaximumHeight( options.get('numLines', 5) * 20 )
        vbox.addWidget(self._editor, 1)

        # vbox.addStretch(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vbox)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)

        self.updateEditorValue()

        # we get lots of 'editingFinished' events,
        # so filter to only generate undos for important ones.

        self._value = self._editor.toPlainText()
        def invokeSetter():
            value = self._editor.toPlainText()
            if self._value != value:
                self._value = value
                self._setValueToController()
        self._editor.textChanged.connect(self._setValueToController)

        self.setEditable( valueController.isEditable() )


    def setEditable(self, editable):
        self._editor.setReadOnly( not editable )


    def getEditorValue(self):
        return self._editor.toPlainText()


    def setEditorValue(self, value):
        self._editor.setText(value)


    def getColumnSpan(self):
        """Returns the number of columns in the layout grid this widget takes up. Wide widgets can return values greater than 1 to modify thier alignment relative to the label."""
        return 2


    @classmethod
    def canDisplay(cls, valueController):
        if valueController.getDataType() == 'String':
            if valueController.hasOption('multiLine'):
                return True
            else:
                value = valueController.getValue()
                if value.find('\n') > -1:
                    return True
        return False



EditorFactory.registerEditorClass(StringEditor)

