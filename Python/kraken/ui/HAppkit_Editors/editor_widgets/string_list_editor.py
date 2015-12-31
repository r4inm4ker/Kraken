from PySide import QtGui, QtCore

from ..fe import FE
from ..widget_factory import EditorFactory
from ..base_editor import BaseValueEditor


# By importing the array_editor here, we ensure that the array_editor is registered
# before the StringListEditor, meaning the StringListEditor will take precedence when displaying values with the 'Combo' option.
# The registered widgets are checked in reverse order, so that the last registered widgets are checked first.
# this makes it easy to override an existing widget by implimenting a new one and importing the widget you wish to overeride.
import array_editor

class StringListEditor(BaseValueEditor):

    def __init__(self, valueController, parent=None):
        super(StringListEditor, self).__init__(valueController, parent=parent)


        hbox = QtGui.QHBoxLayout()
        self._editor = QtGui.QListWidget(self)
        if self._valueController.hasOption('maxHeight'):
            self._editor.setMaximumHeight(self._valueController.getOption('maxHeight', 65))
            self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        else:
            self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)

        hbox.addWidget(self._editor, 1)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)

        self.updateEditorValue()

        if self.isEditable():
            def setSelectionOption(value):
                self._valueController.setOption('currentItem', value)
            self._editor.itemSelectionChanged.connect(setSelectionOption)
        else:
            self.setEditable(False)

    def setEditable(self, editable):
        self._editor.setEnabled(editable)

    def getEditorValue(self):
        return self.__items


    def setEditorValue(self, value):
        self._updatingEditor = True
        self.__items = value
        self._editor.clear()
        for i in range(len(self.__items)):
            self._editor.addItem(str(self.__items[i]))

        if self._valueController.hasOption('currentItem'):
            self._editor.setCurrentItem(self._editor.item(self._valueController.getOption('currentItem')))
        self._updatingEditor = False


    @classmethod
    def canDisplay(cls, valueController):
        return valueController.getDataType() == 'String[]' and valueController.hasOption('list')



EditorFactory.registerEditorClass(StringListEditor)


