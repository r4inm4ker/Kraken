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
        """Returns the name of the attribute.

        Return:
        String of the name of the attribute.

        """

        return self.name


    # ==============
    # Value Methods
    # ==============
    def getValue(self):
        """Returns the value of the attribute.

        Return:
        Value of the attribute.

        """

        return self.value


    def setValue(self, value):
        """Sets the value of the attribute.

        Arguments:
        value -- Value to set the attribute to.

        Return:
        True if successful.

        """

        self.value = value

        return True


    # ===============
    # Parent Methods
    # ===============
    def getParent(self):
        """Returns the paret of this attribute.

        Return:
        Parent object of this attribute.

        """

        return self.parent


    def setParent(self, parent):
        """Sets the paret of this attribute.

        Arguments:
        parent -- Object, parent object of this attribute.

        Return:
        True if successful.

        """

        self.parent = parent

        return True