import copy
from PySide import QtGui, QtCore
from AttributeWidgetImpl import AttributeWidget
from parameter import Parameter

class ArrayWidget(AttributeWidget):

    def __init__(self, attribute, parentWidget=None, addNotificationListener = True):
        super(ArrayWidget, self).__init__(attribute, parentWidget=parentWidget, addNotificationListener = addNotificationListener)

        self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)


        self._enableAddElements = attribute.getOption('enableAddElements', attribute.getOption('enableAddRemoveElements', True))
        self._enableRemoveElements = attribute.getOption('enableRemoveElements', attribute.getOption('enableAddRemoveElements', True))

        self._addElementButtonLabel = attribute.getOption('addElementButtonLabel', 'add')
        self._removeElementButtonLabel = attribute.getOption('removeElementButtonLabel', 'remove')
        self._displayArrayLimit = self._attribute.getOption('displayArrayLimit', True)
        self._displayNumElements = self._attribute.getOption('displayNumElements', True)
        self._arrayLimit = self._attribute.getOption('arrayLimit', 3)

        self._dataType = attribute.getDataType()
        self._valueArray = self._invokeGetter()
        self.determineElementType()

        vbox = QtGui.QVBoxLayout()

        if self._displayArrayLimit or self._attribute.getOption('displayNumElements', True):
            topToolbar = QtGui.QWidget(self)
            topToolbarLayout = QtGui.QHBoxLayout()
            topToolbar.setLayout(topToolbarLayout)
            vbox.addWidget(topToolbar, 0)

            if self._attribute.getOption('displayNumElements', True):
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
        # self._grid.setContentsMargins(0, 0, 0, 0)

        widget = QtGui.QWidget(self)
        widget.setLayout(self._grid)
        vbox.addWidget(widget)

        if self._attribute.getOption('displayGroupbox', True):
            groupBox = QtGui.QGroupBox(self._attribute.getDataType())
            groupBox.setLayout(vbox)
            groupBox.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

            groupBoxLayout = QtGui.QVBoxLayout()
            groupBoxLayout.addWidget(groupBox, 0)
            self.setLayout(groupBoxLayout)
        else:
            self.setLayout(vbox)


        self.build()

    def determineElementType(self):
        # Determine the element value type from the value type of the array.
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


    def build(self):

        self._widgets = []

        for i in range(0, len(self._valueArray)):
            if self._displayArrayLimit and i == self._arrayLimit:
                break
            self.constructAndAddElementWidget(i)

        if self.isEditable() and self._enableAddElements:
            if not self._displayArrayLimit or self._displayArrayLimit and len(self._valueArray) < self._arrayLimit and not self._constSizeArray:
                addElementButton = QtGui.QPushButton(self._addElementButtonLabel, self)
                def addElement():
                    self.getController().beginUndoBracket(name="Add element to :" + self.getLabel())
                    index = len(self._valueArray)

                    newArray = self.getController().constructRTVal(self._dataType)
                    newArray.resize(index + 1)
                    for i in range(index, len(newArray)-1):
                        newArray[i] = self._valueArray[i]

                    try:
                        # If the element type is an object, then we should create it here.
                        newValue = self.getController().constructRTVal(self._elementValueType)
                        newArray[index] = newValue
                    except:
                        pass

                    self._valueArray = newArray
                    self._invokeSetter()

                    self.getController().endUndoBracket()
                    self.rebuild()

                addElementButton.clicked.connect(addElement)
                self._grid.addWidget(addElementButton, len(self._valueArray), 1, 1, 2)


    def constructElementWidget(self, index):
        def elementGetter():
            return self._valueArray[index]
        elementSetter = None

        if self.isEditable():
            def elementSetter(value):
                self._valueArray[index] = value
                self._invokeSetter(self._valueArray)
        elementParameter = Parameter(
            controller=self.getController(),
            name=str(index),
            portType=self._attribute.getPortType(),
            dataType=self._elementValueType,
            getterFn=elementGetter,
            setterFn=elementSetter
        )
        return AttributeWidget.constructAttributeWidget(self.getController(), elementParameter, parentWidget=self, addNotificationListener=False)

    def constructAndAddElementWidget(self, index):
        elementWidget = self.constructElementWidget(index)

        self._grid.addWidget(QtGui.QLabel(str(index), self), index, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        if elementWidget is not None:
            self._grid.addWidget(elementWidget, index, 1)

        if self.isEditable() and self._enableRemoveElements and not self._constSizeArray:
            removeElementButton = QtGui.QPushButton(self._removeElementButtonLabel, self)
            def removeElement():
                self.getController().beginUndoBracket(name="Remove element from :" + self.getLabel())

                client = self.getController().getClient()
                newArray = self.getController().constructRTVal(self._dataType)
                newArray.resize(len(self._valueArray) - 1)
                for i in range(index, len(newArray)):
                    newArray[i] = self._valueArray[i+1]
                self._valueArray = newArray
                self._invokeSetter()

                self.getController().endUndoBracket()
                self.rebuild()

            removeElementButton.clicked.connect(removeElement)

            self._grid.addWidget(removeElementButton, index, 2)

        if elementWidget is not None:
            self._widgets.append(elementWidget)

    def rebuild(self):
        """ Rebuild the sub-widgets because the number of elements in the array changed."""
        # first clear the layout and then build again.
        for i in range(0, len(self._widgets)):
            self._widgets[i].unregisterNotificationListener()

        while self._grid.count():
            self._grid.takeAt(0).widget().deleteLater()

        self.build()

    def getWidgetValue(self):
        return self._valueArray

    def setWidgetValue(self, valueArray):
        self._valueArray = valueArray
        if not len(self._valueArray) == len(self._widgets):
            self.rebuild()
        else:
            for i in range(len(valueArray)):
                if i < len(self._widgets):
                    self._widgets[i].setWidgetValue(valueArray[i])

    def getColumnSpan(self):
        """Returns the number of columns in the layout grid this widget takes up. Wide widgets can return values greater than 1 to modify thier alignment relative to the label."""
        return 2

    def unregisterNotificationListener(self):
        """
        When the widget is being removed from the inspector,
        this method must be called to unregister the event handlers
        """
        for i in range(len(self._widgets)):
            self._widgets[i].unregisterNotificationListener()
        super(ArrayWidget, self).unregisterNotificationListener()


    @classmethod
    def canDisplay(cls, attribute):
        dataType = attribute.getDataType()
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



ArrayWidget.registerPortWidget()

