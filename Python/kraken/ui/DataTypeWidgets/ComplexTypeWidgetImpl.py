import json
from PySide import QtCore, QtGui
from NestedWidgetImpl import NestedWidget
import FabricEngine.Core as Core

class ComplexTypeWidget(NestedWidget):

    def __init__(self, attribute, parentWidget=None, addNotificationListener = True):
        super(ComplexTypeWidget, self).__init__(attribute, parentWidget=parentWidget, addNotificationListener = addNotificationListener)

        self.__typeDesc = None
        try:
            self.__typeDesc = json.loads(attribute.getValue().type("Type").jsonDesc("String"))
        except Exception as e:
            print e
        if self.__typeDesc is None:
            raise Exception("Invalid valuetype specified when constructing ComplexTypeWidget for value '" + attribute.getName() + "' of type '" + str(attribute.getDataType()) +"'")

        self.expanded = False
        def showMemberWidgets():
            for i in range(0, len(self.__typeDesc['members'])):
                try:
                    memberName = self.__typeDesc['members'][i]['name']
                    memberType = self.__typeDesc['members'][i]['type']
                    if str(getattr(self._value, memberName)) != '<RTVal:null>':
                        self.addMemberWidget(memberName, memberType)
                except Exception as e:
                    print e
            self.expanded = True
        def hideMembeWidgets():
            self.clear()
            self.expanded = False


        # self._grid.addWidget(QtGui.QLabel(attribute.getDataType()+':', self), self._gridRow, 0)

        self.expandButton = QtGui.QPushButton("+", self)
        self.expandButton.setCheckable(True)
        self.expandButton.setMinimumHeight(16)
        self.expandButton.setMaximumHeight(16)
        self.expandButton.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed))

        topToolbar = QtGui.QWidget(self)
        topToolbarLayout = QtGui.QHBoxLayout()
        topToolbar.setLayout(topToolbarLayout)
        topToolbarLayout.addWidget(self.expandButton, 0)
        topToolbarLayout.addStretch(2)

        self._grid.addWidget(topToolbar, self._gridRow, 0)
        self._gridRow += 1
        def expandButtonToggled(toggled):
            if toggled:
                self.expandButton.setText('-')
                showMemberWidgets()
            else:
                self.expandButton.setText('+')
                hideMembeWidgets()
        self.expandButton.toggled.connect(expandButtonToggled)

        self._value = attribute.getValue()

    def getWidgetValue(self):
        if self.expanded:
            klType = self.getController().getType(self._dataType)
            for i in range(0, len(self.__typeDesc['members'])):
                memberName = self.__typeDesc['members'][i]['name']
                memberValue = self._widgets[memberName].getWidgetValue()
                if type(memberValue) == Core.CAPI.RTVal and memberValue.isNullObject():
                    continue
                setattr(self._value, memberName, memberValue)
        return self._value

    def setWidgetValue(self, value):
        if self.expanded:
            self._value = value
            for attrDesc in self.__typeDesc['members']:
                attrName = attrDesc['name']
                self._widgets[attrName].setWidgetValue(getattr(value, attrName))

    @classmethod
    def canDisplay(cls, attribute):
        value = attribute.getValue()
        try:
            if value.isObject() and value.isNullObject():
                return False
            # if type(value) != Core.CAPI.RTVal or value.isNullObject():
            #     return False
            typeDesc = json.loads(attribute.getValue().type("Type").jsonDesc("String"))
            if 'members' in typeDesc:
                return True
        except Exception as e:
            return False

ComplexTypeWidget.registerPortWidget()