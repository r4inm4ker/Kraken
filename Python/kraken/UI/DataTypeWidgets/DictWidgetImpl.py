import copy
from PySide import QtGui, QtCore
from AttributeWidgetImpl import AttributeWidget

from parameter import Parameter

class DictWidget(AttributeWidget):

    def __init__(self, attribute, parentWidget=None, addNotificationListener = True):
        super(DictWidget, self).__init__(attribute, parentWidget=parentWidget, addNotificationListener = addNotificationListener)

        vbox = QtGui.QVBoxLayout()
        vbox.setSpacing(2)

        self.setLayout(vbox)

        self._grid = QtGui.QGridLayout()
        self._grid.setContentsMargins(0, 0, 0, 0)

        gridWidget = QtGui.QWidget(self)
        gridWidget.setLayout(self._grid)
        vbox.addWidget(gridWidget, 1)

        self.setLayout(self._grid)
        self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)

        self.__enableAddRemoveElements = attribute.getOption('enableAddRemoveElements', True)
        self.__addElementButtonLabel = attribute.getOption('addElementButtonLabel', 'add')
        self.__removeElementButtonLabel = attribute.getOption('removeElementButtonLabel', 'remove')
        self.__defaultKeyValue = attribute.getOption('defaultKeyValue', 'key')

        self._dataType  = attribute.getDataType()

        # print attribute.getOwner().getScene().getFabricClient().RT.getAggregateMemberInfo(self._dataType)
        # raise Exception("Foo")

        self.determineElementType()
        self.build()


    def determineElementType(self):
        # Determine the element value type from the value type of the array.
        openBraceIdx = self._dataType.find('[')
        closeBraceIdx = self._dataType.find(']')
        keyType = self._dataType[openBraceIdx+1:closeBraceIdx]
        self._elementValueType = self._dataType.replace('['+keyType+']', '', 1)

    def build(self):
        self.__value = self._invokeGetter()
        self.__keywidgets = {}
        self.__widgets = {}
        # this dictionary maps the keys used in the initial dict passed in, and the new keys as the are modified in the UI.
        # this is required because you can't modify the 'attrName' value defined in the closure below.
        self.__attrNameMapping = {}

        def constructWidget(index, attrName, attrValueType):

            self.__attrNameMapping[attrName] = attrName
            def keyGetter():
                return attrName

            if self.isEditable():
                def keySetter(key):
                    value = self.__value[self.__attrNameMapping[attrName]]
                    del self.__value[self.__attrNameMapping[attrName]]
                    self.__value[key] = value

                    keyWidget = self.__keywidgets[self.__attrNameMapping[attrName]]
                    valueWidget = self.__widgets[self.__attrNameMapping[attrName]]
                    del self.__keywidgets[self.__attrNameMapping[attrName]]
                    del self.__widgets[self.__attrNameMapping[attrName]]
                    self.__keywidgets[key] = keyWidget
                    self.__widgets[key] = valueWidget
                    self.__attrNameMapping[attrName] = key
                    self._invokeSetter(self.__value)
            else:
                keySetter = None

            # sub-widgets should initialize their values.
            keyParam = Parameter(
                    controller=self.getController(),
                    name="",
                    portType=self._attribute.getPortType(),
                    dataType = 'String',
                    getterFn = keyGetter,
                    setterFn = keySetter
                )
            keyWidget = AttributeWidget.constructAttributeWidget(self.getController(), keyParam, parentWidget=self, addNotificationListener=False)

            def valueGetter():
                return self.__value[self.__attrNameMapping[attrName]]
            if self.isEditable():
                def valueSetter(value):
                    self.__value[self.__attrNameMapping[attrName]] = value
                    self._invokeSetter(self.__value)
            else:
                valueSetter = None

            valueParam = Parameter(
                    controller=self.getController(),
                    name="",
                    portType=self._attribute.getPortType(),
                    dataType = attrValueType,
                    getterFn = valueGetter,
                    setterFn = valueSetter
                )
            valueWidget = AttributeWidget.constructAttributeWidget(self.getController(), valueParam, parentWidget=self, addNotificationListener=False)

            # self._grid.addWidget(QtGui.QLabel(attrName, self), index, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
            self._grid.addWidget(keyWidget, index, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
            self._grid.addWidget(valueWidget, index, 1)
            self.__keywidgets[attrName] = keyWidget
            self.__widgets[attrName] = valueWidget

            if self.isEditable() and self.__enableAddRemoveElements:
                removeElementButton = QtGui.QPushButton(self.__removeElementButtonLabel, self)
                def removeElement():
                    self.getController().beginUndoBracket(name="Remove element from :" + self.getLabel())

                    newDict = self.getController().constructRTVal(self._dataType)
                    for key in self.__value:
                        if key != attrName:
                            newDict[key] = self.__value[key]

                    self.__value = newDict
                    self._invokeSetter()

                    self.getController().endUndoBracket()
                    self.rebuild()

                removeElementButton.clicked.connect(removeElement)
                self._grid.addWidget(removeElementButton, index, 2)

        index = 0
        for attrName in self.__value:
            constructWidget(index, attrName, self._elementValueType)
            index = index + 1

        if self.isEditable() and self.__enableAddRemoveElements:
            addElementButton = QtGui.QPushButton(self.__addElementButtonLabel, self)
            def addElement():
                self.getController().beginUndoBracket(name="Add element to :" + self.getLabel())

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

                newDict = self.getController().constructRTVal(self._dataType)
                for key in self.__value:
                    newDict[str(key)] = self.__value[str(key)]

                # Caused a crash (TODO: log bug for Andrew)
                # newDict = self.__value.clone(self._dataType)

                newValue = self.getController().constructRTVal(self._elementValueType)
                if newValue is None:
                    raise Exception("Invalid element type:" + self._elementValueType)

                newDict[str(newValueKey)] = newValue

                self.__value = newDict
                self._invokeSetter()

                self.getController().endInteraction()
                self.rebuild()

            addElementButton.clicked.connect(addElement)
            self._grid.addWidget(addElementButton, index, 0)


    def rebuild(self):
        """ Rebuild the sub-widgets because the structure of elements has changed."""
        # first clear the layout and then build again.
        for attrName in self.__widgets:
            self.__widgets[attrName].unregisterNotificationListener()
        while self._grid.count():
            self._grid.takeAt(0).widget().deleteLater()

        self.build()

    def getWidgetValue(self):
        return self.__value

    def setWidgetValue(self, value):
        # Rebuild the UI if there is a key in the value that id not
        # represented in the widgets, or if there is a widget not
        # represented in the value.
        for attrName in value:
            if attrName not in self.__widgets:
                self.rebuild()
                return
        for attrName in self.__widgets:
            if attrName not in value:
                self.rebuild()
                return

        # Update the existing widget values.
        for attrName in value:
            self.__keywidgets[attrName].setWidgetValue(attrName)
            self.__widgets[attrName].setWidgetValue(value[attrName])
        self.__value = value

    def unregisterNotificationListener(self):
        """
        When the widget is being removed from the inspector,
        this method must be called to unregister the event handlers
        """
        for widget in self.__widgets:
            self.__widgets[widget].unregisterNotificationListener()
        super(DictWidget, self).unregisterNotificationListener()

    @classmethod
    def canDisplay(cls, attribute):
        dataType = attribute.getDataType()
        openBraceIdx = dataType.find('[')
        closeBraceIdx = dataType.find(']')
        if closeBraceIdx > openBraceIdx+1:
            keyType = dataType[openBraceIdx+1:closeBraceIdx]
            if keyType == 'String':
                return True
        return False

DictWidget.registerPortWidget()
