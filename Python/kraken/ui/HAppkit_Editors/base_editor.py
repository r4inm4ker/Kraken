from PySide import QtGui

from core.undo_redo_manager import UndoRedoManager, Command

class BaseValueEditor(QtGui.QWidget):

    def __init__(self, valueController, parent=None):
        super(BaseValueEditor, self).__init__(parent)

        self._valueController = valueController
        self._dataType = valueController.getDataType()

        self._updatingEditor = False
        self._firingSetter = False
        self.__interactionInProgress = False

        self._valueController.valueChanged.connect(self._onValueChange)
        self._valueController.editableChanged.connect(self.setEditable)


    def isEditable(self):
        return self._valueController.isEditable()


    def setEditable(self, editable):
        self.setEnabled(editable)


    def getName(self):
        return self._valueController.getName()


    def updateEditorValue(self):
        self.setEditorValue(self._invokeGetter())


    def setEditorValue(self, value):
        """This method is used to update the value displayed by the widget. Must be defined in a derived class"""
        raise NotImplementedError("setEditorValue not implimented: "+self.__name)


    def getEditorValue(self):
        """This method is used to return the value displayed in the widget. Must be defined in a derived class"""
        raise NotImplementedError("getEditorValue not implimented: "+self.__name)


    def _invokeGetter(self):
        return self._valueController.getValue()


    def _onValueChange(self, value):
        """This method is fired when the port has changed and the widget needs to be updated to display the new value"""

        # TODO: some widgets may want to override the updated value, but this behavior makes editing string widgets really annoying
        # as it re-focusses the widget after every change. I made '_onValueChange' protected so that derived widgets can override it.
        if not self.__interactionInProgress and not self._firingSetter:
            self._updatingEditor = True
            self.setEditorValue(value)
            self._updatingEditor = False


    def beginInteraction(self):
        UndoRedoManager.getInstance().openBracket(self._valueController.getName() + " changed")
        self.__interactionInProgress = True


    def endInteraction(self):
        self.__interactionInProgress = False
        UndoRedoManager.getInstance().closeBracket()


    def _setValueToController(self, value = None):
        if self._updatingEditor:
            return
        # interactionInProgress = self.__interactionInProgress
        # if not interactionInProgress:
        #     self.beginInteraction()

        self._firingSetter  = True
        # some value changes, such as resizing arrays, requires that the widget be re-built.
        # in those cases, we should provide the value to the setter.
        # if value is None:
        # For now this is disabled, because we always want to set an RTVal on the valueController.
        # (getEditorValue should now always return an RTVal)
        value = self.getEditorValue()
        self._valueController.setValue(value)

        self._firingSetter  = False

        # if not interactionInProgress:
        #     self.endInteraction()


    # def getMinLabelWidth(self):
    #     return self._minLabelWidth


    # def setMinLabelWidth(self, value):
    #     self._minLabelWidth = value


    def getRowSpan(self):
        """Returns the number of rows in the layout grid this widget takes up."""
        return 1


    def getColumnSpan(self):
        """Returns the number of columns in the layout grid this widget takes up. Wide widgets can return values greater than 1 to modify thier alignment relative to the label."""
        return 1


    @classmethod
    def canDisplay(cls, valueController):
        """Must be overridden for every subclasses"""
        raise NotImplementedError("Class method 'canDisplay()' must be implemented in widget: " + str(cls))

