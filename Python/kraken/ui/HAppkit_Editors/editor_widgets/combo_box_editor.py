from PySide import QtGui, QtCore

from ..fe import FE
from ..widget_factory import EditorFactory
from ..base_editor import BaseValueEditor


class ComboBoxEditor(BaseValueEditor):

    def __init__(self, valueController, parent=None):
        super(ComboBoxEditor, self).__init__(valueController, parent=parent)


        self.__name = valueController.getName()
        self._items = []

        hbox = QtGui.QHBoxLayout()

        self._editor = QtGui.QComboBox(self)
        hbox.addWidget(self._editor, 1)

        hbox.addStretch(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)

        items = valueController.getOption('combo')
        if items is not None:
            self.setComboBoxItems(items)
            self.updateEditorValue()

        self._editor.currentIndexChanged.connect(self._setValue)
        self.setEditable(self.isEditable())

    def setEditable(self, editable):
        self._editor.setEnabled( not editable )


    def _setValue(self):
        # In the case of a combo box with no items, we still get 'currentIndexChanged' events,
        # but must filter tem out here. We also don't want to propagate changes back to the
        # scene when updating the combo box items.
        if len(self._items) == 0 or self._updatingEditor:
            return
        self._setValueToController()


    def setComboBoxItems(self, items):
        self._updatingEditor = True
        # Store the previous item, so we can maintain the selection after updating.
        currentItem = None
        if self._items is not None and self._editor.currentIndex() >= 0 and self._editor.currentIndex() < len(self._items):
            currentItem = self._items[self._editor.currentIndex()]
        self._editor.clear()
        index = 0
        for item in items:
            self._editor.addItem(item)
            if item == currentItem:
                # restore the previous selection
                self._editor.setCurrentIndex(int(value))
            index = index + 1
        self._items = items
        self.setStyleSheet("QComboBox QAbstractItemView  { min-height: " + str(len(self._items)) + "px; }")
        self._updatingEditor = False


    def getEditorValue(self):
        return self._editor.currentIndex()


    def setEditorValue(self, value):
        self._updatingEditor = True
        self._editor.setCurrentIndex(int(value))
        self._updatingEditor = False


    @classmethod
    def canDisplay(cls, valueController):
        return valueController.hasOption('combo') and (
                    valueController.getDataType() == 'Integer' or
                    valueController.getDataType() == 'UInt8' or
                    valueController.getDataType() == 'SInt8' or
                    valueController.getDataType() == 'UInt16' or
                    valueController.getDataType() == 'SInt16' or
                    valueController.getDataType() == 'UInt32' or
                    valueController.getDataType() == 'SInt32' or
                    valueController.getDataType() == 'UInt64' or
                    valueController.getDataType() == 'SInt64' or
                    valueController.getDataType() == 'Index' or
                    valueController.getDataType() == 'Size'
                )

EditorFactory.registerEditorClass(ComboBoxEditor)
