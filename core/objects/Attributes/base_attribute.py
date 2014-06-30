"""Kraken - objects.Attributes.BaseAttribute module.

Classes:
BaseAttribute - Base Attribute.

"""

class BaseAttribute(object):
    """Base Attribute object."""

    def __init__(self, name, value):
        super(BaseAttribute, self).__init__()
        self.name = name
        self.value = value
        self.parent = None


    def getName(self):
        return self.name


    # ==============
    # Value Methods
    # ==============
    def getValue(self):
        return self.value


    def setValue(self, value):
        self.value = value

        return True


    # ===============
    # Parent Methods
    # ===============
    def getParent(self):
        return self.parent


    def setParent(self, parent):
        self.parent = parent

        return True