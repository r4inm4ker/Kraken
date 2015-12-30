import copy
from PySide import QtGui, QtCore

from ..fe import FE
from ..widget_factory import EditorFactory
from ..base_editor import BaseValueEditor
from ..core.undo_redo_manager import UndoRedoManager
from ..core.value_controller import ElementController

class ArrayEditor(BaseValueEditor):

    def __init__(self, valueController, parent=None):
        super(ArrayEditor, self).__init__(valueController, parent=parent)

        self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)

        self._enableAddElements = True #valueController.getOption('enableAddElements', valueController.getOption('enableAddRemoveElements', True))
        self._enableRemoveElements = True #valueController.getOption('enableRemoveElements', valueController.getOption('enableAddRemoveElements', True))

        self._addElementButtonLabel = 'add' #valueController.getOption('addElementButtonLabel', 'add')
        self._removeElementButtonLabel = 'remove' #valueController.getOption('removeElementButtonLabel', 'remove')

        self._displayGroupBox = False #self._valueController.getOption('displayArrayLimit', True)
        self._displayIndex = False #self._valueController.getOption('displayArrayLimit', True)
        self._displayArrayLimit = False #self._valueController.getOption('displayArrayLimit', True)
        self._displayNumElements = False #self._valueController.getOption('displayNumElements', True)
        self._arrayLimit = 3 #self._valueController.getOption('arrayLimit', 3)

        self._dataType = valueController.getDataType()

        self._valueArray = self._invokeGetter()
        self.determineElementType()

        vbox = QtGui.QVBoxLayout()

        if self._displayArrayLimit or self._displayNumElements:
            topToolbar = QtGui.QWidget(self)
            topToolbarLayout = QtGui.QHBoxLayout()
            topToolbar.setLayout(topToolbarLayout)
            vbox.addWidget(topToolbar, 0)

            if self._displayNumElements:
                topToolbarLayout.addWidget(QtGui.QLabel('Num Elements:'+str(len(self._valueArray)), self))

            if self._displayArrayLimit:
                # display a widget to enable setting the maximum number of displayed elements.

                label = QtGui.QLabel('Max Displayed elements:', self)
                # label.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
                topToolbarLayout.addWidget(label, 0)

                spinBox = QtGui.QSpinBox(self)
                spinBox.setMinimum(0)
                spinBox.setMaximum(100)
                # spinBox.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
                spinBox.setValue(self._arrayLimit)
                def setArrayLimit(value):
                    self._arrayLimit = value
                    self.rebuild()
                spinBox.valueChanged.connect(setArrayLimit)
                topToolbarLayout.addWidget(spinBox, 0)
            topToolbarLayout.addStretch(1)

        self._grid = QtGui.QGridLayout()
        self._grid.setContentsMargins(0, 0, 0, 0)

        widget = QtGui.QWidget(self)
        widget.setLayout(self._grid)
        vbox.addWidget(widget)

        if self._displayGroupBox:
            groupBox = QtGui.QGroupBox(self._valueController.getDataType())
            groupBox.setLayout(vbox)
            groupBox.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

            groupBoxLayout = QtGui.QVBoxLayout()
            groupBoxLayout.addWidget(groupBox, 0)
            self.setLayout(groupBoxLayout)
        else:
            self.setLayout(vbox)


        self.build()

        if self._elementValueType == 'String':
            self.setAcceptDrops(self.isEditable())

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()

    def dropEvent(self, viewport, event):
        if event.mimeData().hasText():

            undoManager = UndoRedoManager.getInstance()
            undoManager.openBracket("Add element to :" + self.getName())
            self.addElement()
            self._valueArray[len(self._valueArray) - 1] = event.mimeData().text()
            self._setValueToController()

            undoManager.closeBracket()
            self.rebuild()

            event.acceptProposedAction()


    def determineElementType(self):
        # Determine the element value type from the value type of the array.
        if self._dataType.endswith('Array'):
            self._elementValueType = self._dataType[:len(self._dataType)-5]
            self._constSizeArray = False
        else:
            openBraceIdx = self._dataType.find('[')
            closeBraceIdx = self._dataType.find(']')
            keyType = ''
            self._constSizeArray = False
            if closeBraceIdx > openBraceIdx+1:
                try:
                    keyType = self._dataType[openBraceIdx+1:closeBraceIdx]
                    int(keyType)
                    self._constSizeArray = True
                except:
                    raise Exception("Value type is not an array:'" + self._dataType + "'")
            self._elementValueType = self._dataType.replace('['+keyType+']', '', 1)


    def addElement(self):
        index = len(self._valueArray)

        newArray = FE.getInstance().rtVal(self._dataType)
        newArray.resize(index + 1)
        for i in range(0, len(newArray)-1):
            newArray[i] = self._valueArray[i]

        try:
            # If the element type is an object, then we should create it here.
            newValue = FE.getInstance().rtVal(self._elementValueType)
            newArray[index] = newValue
        except:
            pass

        self._valueArray = newArray


    def removeElement(self, index):
        newArray = FE.getInstance().rtVal(self._dataType)
        newArray.resize(len(self._valueArray) - 1)

        for i in range(0, index):
            newArray[i] = self._valueArray[i]

        for i in range(index, len(newArray)):
            newArray[i] = self._valueArray[i+1]

        self._valueArray = newArray

    def build(self):

        self._editors = []

        for i in range(0, len(self._valueArray)):
            if self._displayArrayLimit and i == self._arrayLimit:
                break
            self.constructAndAddElementEditor(i)

        if self.isEditable() and self._enableAddElements:
            if not self._displayArrayLimit or self._displayArrayLimit and len(self._valueArray) < self._arrayLimit and not self._constSizeArray:
                self.addElementButton = QtGui.QPushButton(self._addElementButtonLabel, self)
                def addElement():
                    undoManager = UndoRedoManager.getInstance()
                    undoManager.openBracket("Add element to :" + self.getName())

                    self.addElement()
                    self._setValueToController()

                    undoManager.closeBracket()
                    self.rebuild()

                self.addElementButton.clicked.connect(addElement)
                if self._displayIndex:
                    self._grid.addWidget(self.addElementButton, len(self._valueArray), 1, 1, 2)
                else:
                    self._grid.addWidget(self.addElementButton, len(self._valueArray), 0, 1, 2)


    def constructElementEditor(self, index):
        elementController = ElementController(index, self._elementValueType, self._valueArray, self.isEditable())

        def elementChanged(value):
            self._setValueToController()

        elementController.valueChanged.connect(elementChanged)
        return EditorFactory.constructEditor(elementController, parent=self)


    def constructAndAddElementEditor(self, index):
        elementEditor = self.constructElementEditor(index)

        row = index
        column = 0
        if self._displayIndex:
            self._grid.addWidget(QtGui.QLabel(str(index), self), row, column, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
            column += 1
        if elementEditor is not None:
            self._grid.addWidget(elementEditor, row, column)
            column += 1

        if self.isEditable() and self._enableRemoveElements and not self._constSizeArray:
            self.removeElementButton = QtGui.QPushButton(self._removeElementButtonLabel, self)
            def removeElement():

                undoManager = UndoRedoManager.getInstance()
                undoManager.openBracket("Remove element from :" + self.getName())

                self.removeElement(index)
                self._setValueToController()

                undoManager.closeBracket()
                self.rebuild()

            self.removeElementButton.clicked.connect(removeElement)

            self._grid.addWidget(self.removeElementButton, row, column)

        if elementEditor is not None:
            self._editors.append(elementEditor)


    def rebuild(self):
        """ Rebuild the sub-widgets because the number of elements in the array changed."""

        while self._grid.count():
            self._grid.takeAt(0).widget().deleteLater()

        self.build()


    def getEditorValue(self):
        return self._valueArray


    def setEditorValue(self, valueArray):
        self._valueArray = valueArray
        if not len(self._valueArray) == len(self._editors):
            self.rebuild()
        else:
            for i in range(len(valueArray)):
                if i < len(self._editors):
                    self._editors[i].setEditorValue(valueArray[i])


    def getColumnSpan(self):
        """Returns the number of columns in the layout grid this widget takes up. Wide widgets can return values greater than 1 to modify thier alignment relative to the label."""
        return 2


    @classmethod
    def canDisplay(cls, valueController):
        dataType = valueController.getDataType()
        if dataType.endswith('Array'):
            return True

        openBraceIdx = dataType.find('[')
        closeBraceIdx = dataType.find(']')
        if closeBraceIdx == openBraceIdx+1:
            return True
        if closeBraceIdx > openBraceIdx+1:
            try:
                keyType = dataType[openBraceIdx+1:closeBraceIdx]
                constInt = int(keyType)
                return True
            except:
                return False
        return False


EditorFactory.registerEditorClass(ArrayEditor)

