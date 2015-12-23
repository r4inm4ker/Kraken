
#
# Copyright 2015 Horde Software Inc. All rights reserved.
#

import json
from value_controller import ValueController



class PyValController(ValueController):

    def __init__(self, name, dataType, value, desc=None, parent=None, **kwargs):
        super(PyValController, self).__init__(name, dataType, parent=parent, **kwargs)
        self.value = value
        self.__desc = desc

    def _setValue_NoUndo(self, value):
        self.value = value
        self.valueChanged.emit(value)

    def getValue(self):
        return self.value

