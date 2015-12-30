import json
from PySide import QtCore, QtGui

from ..fe import FE
from ..widget_factory import EditorFactory
from nested_editor import NestedEditor
import FabricEngine.Core as Core

class ComplexTypeEditor(NestedEditor):

    def __init__(self, valueController, parent=None):
        super(ComplexTypeEditor, self).__init__(valueController, parent=parent)

        self.__typeDesc = None
        try:
            self.__typeDesc = json.loads(valueController.getValue().type('Type').jsonDesc('String'))
        except Exception as e:
            print e
        if self.__typeDesc is None:
            raise Exception("Invalid valuetype specified when constructing ComplexTypeEditor for value '" + valueController.getName() + "' of type '" + str(valueController.getDataType()) +"'")

        self.expanded = False
        def showMemberEditors():
            for i in range(0, len(self.__typeDesc['members'])):
                try:
                    memberName = self.__typeDesc['members'][i]['name']
                    memberType = self.__typeDesc['members'][i]['type']
                    if str(getattr(self._value, memberName)) != '<RTVal:null>':
                        self.addMemberEditor(memberName, memberType)
                except Exception as e:
                    print e
            self.expanded = True

        def hideMembeEditors():
            self.clear()
            self.expanded = False


        # self._grid.addWidget(QtGui.QLabel(valueController.getDataType()+':', self), self._gridRow, 0)

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
                showMemberEditors()
            else:
                self.expandButton.setText('+')
                hideMembeEditors()
        self.expandButton.toggled.connect(expandButtonToggled)

        self._value = valueController.getValue()


    def getEditorValue(self):
        if self.expanded:
            klType = FE.getInstance().types()[self._dataType]
            for i in range(0, len(self.__typeDesc['members'])):
                memberName = self.__typeDesc['members'][i]['name']
                memberValue = self._editors[memberName].getEditorValue()
                if type(memberValue) == Core.CAPI.RTVal and str(memberValue.type('Type')) == '<RTVal:null>': # memberValue.isNullObject():
                    continue
                setattr(self._value, memberName, memberValue)
        return self._value


    def setEditorValue(self, value):
        if self.expanded:
            self._value = value
            for attrDesc in self.__typeDesc['members']:
                attrName = attrDesc['name']
                self._editors[attrName].setEditorValue(getattr(value, attrName))


    @classmethod
    def canDisplay(cls, valueController):
        try:
            value = valueController.getValue()
            if str(type(value)) == "<type 'PyRTValObject'>":
                typeDesc = json.loads(value.type('Type').jsonDesc('String'))
                if 'members' in typeDesc:
                    return True
        except Exception as e:
            return False

EditorFactory.registerEditorClass(ComplexTypeEditor)