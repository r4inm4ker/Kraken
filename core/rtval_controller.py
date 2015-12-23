
#
# Copyright 2015 Horde Software Inc. All rights reserved.
#

import json
from value_controller import ValueController


class RTValController(ValueController):

    def __init__(self, name, dataType, value, editable=True, **kwargs):
        super(RTValController, self).__init__(name, dataType=dataType, editable=editable, **kwargs)
        self.rtval = value


    def _setValue_NoUndo(self, value):
        self.rtval = value
        self.valueChanged.emit(self.getValue())


    def getValue(self):
        return self._extractSimpleTypes(self.rtval)


    def setRTVal(self, rtval):
        self.rtval = rtval
        self.valueChanged.emit(self.getValue())


class RTValGetterSetterController(ValueController):

    def __init__(self, name, dataType, getter=None, setter=None, **kwargs):
        super(RTValGetterSetterController, self).__init__(name, dataType=dataType, editable=(getter is not None and setter is not None), **kwargs)
        self.getter = getter
        self.setter = setter
        self.rtval = None
        if self.getter is None:
            self.rtval = FE.getInstance().rtVal( dataType )


    def _setValue_NoUndo(self, value):
        if self.setter is None:
            self.rtval = value
        else:
            self.setter( '', value )
        self.valueChanged.emit( self.getValue() )


    def getValue(self):
        if self.getter is None:
            return self._extractSimpleTypes(self.rtval)
        else:
            return self._extractSimpleTypes(self.getter( self.getDataType() ))


    def setGetter(self, getter ):
        self.getter = getter
        self.rtval = self.getter( self.getDataType() )
        self.valueChanged.emit(self.getValue())


    def setGetterSetter(self, getter, setter ):
        self.getter = getter
        self.setter = setter
        self.rtval = getter( self.getDataType() )
        self.setEditable( self.setter is not  None )
        self.valueChanged.emit( self.getValue() )
