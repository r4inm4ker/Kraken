import copy
from PySide import QtGui, QtCore

from ..fe import FE
from ..widget_factory import EditorFactory
from ..base_editor import BaseValueEditor
from ..core.undo_redo_manager import UndoRedoManager
from ..core.value_controller import GetterSetterController


class DictEditor(BaseValueEditor):

    def __init__(self, valueController, parent=None):
        super(DictEditor, self).__init__(valueController, parent=parent)

        vbox = QtGui.QVBoxLayout()
        vbox.setSpacing(2)

        self.setLayout(vbox)

        self._grid = QtGui.QGridLayout()
        self._grid.setContentsMargins(0, 0, 0, 0)

        gridEditor = QtGui.QWidget(self)
        gridEditor.setLayout(self._grid)

        vbox.addWidget(gridEditor, 1)

        self.setLayout(self._grid)
        self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)

        self.__enableAddRemoveElements = valueController.getOption('enableAddRemoveElements', True)
        self.__addElementButtonLabel = valueController.getOption('addElementButtonLabel', 'add')
        self.__removeElementButtonLabel = valueController.getOption('removeElementButtonLabel', 'remove')
        self.__defaultKeyValue = valueController.getOption('defaultKeyValue', 'key')

        self._dataType  = valueController.getDataType()

        # print valueController.getOwner().getScene().getFabricClient().RT.getAggregateMemberInfo(self._dataType)

        self.determineElementType()
        self.build()
        self.setEditable( valueController.isEditable() )


    def setEditable(self, editable):
        self.addElementButton.setEnabled(editable)

        for widget in self.__keywidgets:
            widget.setReadOnly( not editable )
        for widget in self.__editors:
            widget.setReadOnly( not editable )
        for widget in self.__removeElementButtons:
            widget.setReadOnly( not editable )


    def determineElementType(self):
        # Determine the element value type from the value type of the array.
        openBraceIdx = self._dataType.find('[')
        closeBraceIdx = self._dataType.find(']')
        keyType = self._dataType[openBraceIdx+1:closeBraceIdx]
        self._elementValueType = self._dataType.replace('['+keyType+']', '', 1)


    def build(self):
        self.__value = self._invokeGetter()
        self.__keywidgets = {}
        self.__editors = {}
        self.__removeElementButtons = {}
        # this dictionary maps the keys used in the initial dict passed in, and the new keys as the are modified in the UI.
        # this is required because you can't modify the 'attrName' value defined in the closure below.
        self.__attrNameMapping = {}

        def constructEditor(index, attrName, attrValueType):

            self.__attrNameMapping[attrName] = attrName
            def keyGetter():
                return attrName

            if self._valueController.isEditable():
                def keySetter(key):
                    if key not in self.__value:

                        newDict = FE.getInstance().rtVal(self._dataType)
                        for currkey in self.__value:
                            if currkey != self.__attrNameMapping[attrName]:
                                newDict[currkey] = self.__value[currkey]
                        newDict[key] = self.__value[self.__attrNameMapping[attrName]]
                        self.__value = newDict

                        self.__keywidgets[key] = self.__keywidgets[self.__attrNameMapping[attrName]]
                        self.__editors[key] = self.__editors[self.__attrNameMapping[attrName]]

                        del self.__keywidgets[self.__attrNameMapping[attrName]]
                        del self.__editors[self.__attrNameMapping[attrName]]
                        self.__attrNameMapping[attrName] = key

                        undoManager = UndoRedoManager.getInstance()
                        if not undoManager.isUndoingOrRedoing():
                            self._setValueToController(self.__value)
                    else:
                        # Put the widget value back to what it was to avoid the collision.
                        keyEditor.setEditorValue(self.__attrNameMapping[attrName])

                # sub-widgets should initialize their values.
                keyController = GetterSetterController(
                        name="",
                        dataType = 'String',
                        getter = keyGetter,
                        setter = keySetter
                    )
            else:
                keyController = GetterSetterController(
                        name="",
                        dataType = 'String',
                        getter = keyGetter
                    )
            keyEditor = EditorFactory.constructEditor(keyController, parent=self)

            def valueGetter():
                return self.__value[self.__attrNameMapping[attrName]]

            if self._valueController.isEditable():
                def valueSetter(value):
                    # Generate a new Dict instead of modifying the existing one.
                    # This is so we don't modifiy a value referenced somewhere in KL
                    newDict = FE.getInstance().rtVal(self._dataType)
                    for currkey in self.__value:
                        if currkey != self.__attrNameMapping[attrName]:
                            newDict[currkey] = self.__value[currkey]
                    newDict[self.__attrNameMapping[attrName]] = value
                    self.__value = newDict

                    undoManager = UndoRedoManager.getInstance()
                    if not undoManager.isUndoingOrRedoing():
                        self._setValueToController(self.__value)

                elementController = GetterSetterController(
                        name="",
                        dataType = attrValueType,
                        getter = valueGetter,
                        setter = valueSetter
                    )
            else:
                elementController = GetterSetterController(
                        name="",
                        dataType = attrValueType,
                        getter = valueGetter
                    )
            valueEditor = EditorFactory.constructEditor(elementController, parent=self)

            # self._grid.addWidget(QtGui.QLabel(attrName, self), index, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
            self._grid.addWidget(keyEditor, index, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
            self._grid.addWidget(valueEditor, index, 1)
            self.__keywidgets[attrName] = keyEditor
            self.__editors[attrName] = valueEditor

            if self.__enableAddRemoveElements:
                removeElementButton = QtGui.QPushButton(self.__removeElementButtonLabel, self)
                def removeElement():
                    undoManager = UndoRedoManager.getInstance()
                    undoManager.openBracket("Remove element from :" + self.getName())
                    newDict = FE.getInstance().rtVal(self._dataType)
                    for key in self.__value:
                        if key != attrName:
                            newDict[key] = self.__value[key]

                    self.__value = newDict
                    self._setValueToController()

                    undoManager.closeBracket()
                    self.rebuild()

                removeElementButton.clicked.connect(removeElement)
                self._grid.addWidget(removeElementButton, index, 2)
                self.__removeElementButtons[attrName] = removeElementButton

        index = 0
        for attrName in self.__value:
            constructEditor(index, attrName, self._elementValueType)
            index = index + 1

        if self.__enableAddRemoveElements:
            self.addElementButton = QtGui.QPushButton(self.__addElementButtonLabel, self)
            def addElement():
                feRtVal = FE.getInstance().rtVal
                undoManager = UndoRedoManager.getInstance()
                undoManager.openBracket("Add element to :" + self.getName())

                # generate a unique key for the new value.
                # Keep interating until a key has been generated that does not collide
                # with any existing keys.
                keyId = 1
                newValueKey = self.__defaultKeyValue
                keyUsed = True
                while keyUsed:
                    found = False
                    for currkey in self.__value:
                        if currkey == newValueKey:
                            newValueKey = self.__defaultKeyValue + str(keyId)
                            found = True
                            keyId += 1
                    keyUsed = found

                newDict = feRtVal(self._dataType)
                for key in self.__value:
                    newDict[str(key)] = self.__value[str(key)]

                # Caused a crash (TODO: log bug for Andrew)
                # newDict = self.__value.clone(self._dataType)

                newValue = feRtVal(self._elementValueType)
                if newValue is None:
                    raise Exception("Invalid element type:" + self._elementValueType)

                newDict[str(newValueKey)] = newValue

                self.__value = newDict
                self._setValueToController()

                undoManager.closeBracket()
                self.rebuild()

            self.addElementButton.clicked.connect(addElement)
            self._grid.addWidget(self.addElementButton, index, 0)


    def rebuild(self):
        """ Rebuild the sub-widgets because the structure of elements has changed."""

        while self._grid.count():
            self._grid.takeAt(0).widget().deleteLater()

        self.build()


    def getEditorValue(self):
        return self.__value


    def setEditorValue(self, value):
        # Rebuild the UI if there is a key in the value that is not
        # represented in the widgets, or if there is a widget not
        # represented in the value.
        for attrName in value:
            if attrName not in self.__editors:
                self.rebuild()
                return
        for attrName in self.__editors:
            if attrName not in value:
                self.rebuild()
                return

        # Update the existing widget values.
        for attrName in value:
            self.__keywidgets[attrName].setEditorValue(attrName)
            self.__editors[attrName].setEditorValue(value[attrName])
        self.__value = value


    @classmethod
    def canDisplay(cls, valueController):
        dataType = valueController.getDataType()
        openBraceIdx = dataType.find('[')
        closeBraceIdx = dataType.find(']')
        if closeBraceIdx > openBraceIdx+1:
            keyType = dataType[openBraceIdx+1:closeBraceIdx]
            if keyType == 'String':
                return True
        return False


EditorFactory.registerEditorClass(DictEditor)
