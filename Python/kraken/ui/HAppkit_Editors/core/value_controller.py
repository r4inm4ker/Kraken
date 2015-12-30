
#
# Copyright 2015 Horde Software Inc. All rights reserved.
#


from PySide import QtCore

from undo_redo_manager import UndoRedoManager, Command

class ValueChangeCommand(Command):
    def __init__(self, valueController, newValue):
        super(ValueChangeCommand, self).__init__()
        self._valueController = valueController
        self.oldValue = self._valueController.getValue()
        self.newValue = newValue


    def shortDesc(self):
        return "Value Change:'" + self._valueController.getName() + "'"


    def redo(self):
        self._valueController._setValue_NoUndo(self.newValue)


    def undo(self):
        self._valueController._setValue_NoUndo(self.oldValue)


    def mergeWith(self, prevCommand):
        if isinstance(prevCommand, ValueChangeCommand):
            if prevCommand._valueController == self._valueController:
                self.newValue = prevCommand.newValue
                self._valueController._setValue_NoUndo(self.newValue)
                return True
        return False


class ValueController(QtCore.QObject):

    valueChanged = QtCore.Signal(object)
    editableChanged = QtCore.Signal(bool)
    optionChanged = QtCore.Signal(str)

    def __init__(self, name, dataType, editable=True, **kwargs):
        super(ValueController, self).__init__()
        self.name = name
        self.dataType = dataType
        self.editable = editable
        self.options = kwargs


    def getName(self):
        return str(self.name)


    def getDataType(self):
        return self.dataType


    def setValue(self, value):
        command = ValueChangeCommand(self, value)
        UndoRedoManager.getInstance().addCommand(command, invokeRedoOnAdd=True)


    def _setValue_NoUndo(self, value):
        raise NotImplementedError()


    def getValue(self):
        raise NotImplementedError()


    def getOption(self, key, defaultValue=None):
        return self.options.get(key, defaultValue)


    def hasOption(self, key):
        return key in self.options


    def setOption(self, key, value):
        self.options[key] = value
        self.optionChanged.emit(key)


    def isEditable(self):
        return self.editable

    def setEditable(self, editable):
        self.editable = editable
        self.editableChanged.emit(editable)


    def _extractSimpleTypes(self, value):
        if  str(type(value)) == "<type 'PyRTValObject'>" and (
            self.dataType == 'Boolean' or \
            self.dataType == 'UInt8' or \
            self.dataType == 'Byte' or \
            self.dataType == 'SInt8' or \
            self.dataType == 'UInt16' or \
            self.dataType == 'SInt16' or \
            self.dataType == 'UInt32' or \
            self.dataType == 'Count' or \
            self.dataType == 'Index' or \
            self.dataType == 'Size' or \
            self.dataType == 'SInt32' or \
            self.dataType == 'Integer' or \
            self.dataType == 'UInt64' or \
            self.dataType == 'DataSize' or \
            self.dataType == 'SInt64' or \
            self.dataType == 'Float32' or \
            self.dataType == 'Scalar' or \
            self.dataType == 'Float64' or \
            self.dataType == 'String'):
            return value
        else:
            return value


    def emitValueChanged(self):
        self.valueChanged.emit(self.getValue())




class MemberController(ValueController):

    def __init__(self, name, dataType, owner, editable=True, **kwargs):
        super(MemberController, self).__init__(name, dataType, editable, **kwargs)
        self.owner = owner


    def _setValue_NoUndo(self, value):
        setattr(self.owner, self.name, value)
        self.valueChanged.emit(self.getValue())


    def getValue(self):
        return self._extractSimpleTypes(getattr(self.owner, self.name))




class ElementController(ValueController):

    def __init__(self, name, dataType, owner, editable=True, **kwargs):
        super(ElementController, self).__init__(name, dataType, editable, **kwargs)
        self.owner = owner


    def _setValue_NoUndo(self, value):
        self.owner[self.name] = value
        self.valueChanged.emit(self.getValue())


    def getValue(self):
        return self._extractSimpleTypes(self.owner[self.name])


class GetterSetterController(ValueController):

    def __init__(self, name, dataType, getter=None, setter=None, defaultValue=None, **kwargs):
        super(GetterSetterController, self).__init__(name, dataType=dataType, editable=(getter is not None and setter is not None), **kwargs)
        self.getter = getter
        self.setter = setter
        self.value = defaultValue


    def _setValue_NoUndo(self, value):
        if self.setter is None:
            self.value = value
        else:
            self.setter( value )
        self.valueChanged.emit( self.getValue() )


    def getValue(self):
        if self.getter is None:
            return self._extractSimpleTypes(self.value)
        else:
            return self._extractSimpleTypes(self.getter())


    def setGetter(self, getter ):
        self.getter = getter
        self.value = self.getter()
        self.valueChanged.emit(self.getValue())


    def setGetterSetter(self, getter, setter ):
        self.getter = getter
        self.setter = setter
        self.value = getter()
        self.setEditable( self.setter is not  None )
        self.valueChanged.emit( self.getValue() )
