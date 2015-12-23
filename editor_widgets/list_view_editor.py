from PySide import QtGui, QtCore

from ..fe import FE
from ..widget_factory import EditorFactory
from ..base_editor import BaseValueEditor


# By importing the ComboBoxEditor here, we ensure that the ComboBoxEditor is registered
# before the ListViewEditor, meaning the ListViewEditor will take precedence when displaying values with the 'Combo' option.
# The registered widgets are checked in reverse order, so that the last registered widgets are checked first.
# this makes it easy to override an existing widget by implimenting a new one and importing the widget you wish to overeride.
import combo_box_editor

class ListViewEditor(BaseValueEditor):

    def __init__(self, valueController, parent=None):
        super(ListViewEditor, self).__init__(valueController, parent=parent)


        hbox = QtGui.QHBoxLayout()
        self._editor = QtGui.QListWidget(self)

        self.__items = valueController.getOption('combo')
        for item in self.__items:
            self._editor.addItem(str(item))
        self._editor.setMaximumHeight(65)

        hbox.addWidget(self._editor, 1)

        hbox.addStretch(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)

        self.updateEditorValue()

        if self.isEditable():
            self._editor.itemSelectionChanged.connect(self._setValueToController)
        else:
            self._editor.setReadOnly(True)


    def getEditorValue(self):
        return self.__items[self._editor.currentRow()]


    def setEditorValue(self, value):
        self._updatingEditor = True
        if value in self.__items:
            index = self.__items.index(value)
        else:
            index = 0
        self._editor.setCurrentItem(self._editor.item(index))
        self._updatingEditor = False


    @classmethod
    def canDisplay(cls, valueController):
        return valueController.getDataType() == 'String' and valueController.hasOption('combo')



EditorFactory.registerEditorClass(ListViewEditor)


