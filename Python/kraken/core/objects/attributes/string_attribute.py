"""Kraken - objects.Attributes.StringAttribute module.

Classes:
StringAttribute - Base Attribute.

"""

from kraken.core.objects.attributes.attribute import Attribute
from kraken.core.kraken_system import ks


class StringAttribute(Attribute):
    """String Attribute. Implemented value type checking."""

    def __init__(self, name, value="", parent=None):
        super(StringAttribute, self).__init__(name, value=value, parent=parent)

        if not isinstance(value, basestring):
            raise TypeError("Value is not of type 'str':" + str(value))


    def setValue(self, value):
        """Sets the value of the attribute.

        Arguments:
        value -- Value to set the attribute to.

        Return:
        True if successful.

        """

        if not isinstance(value, basestring):
            raise TypeError("Value is not of type 'str':" + str(value))

        super(StringAttribute, self).setValue(str(value))

        return True


    def getRTVal(self):
        """Returns and RTVal object for this attribute.

        Return:
        RTVal

        """
        return ks.rtVal('String', self._value)



    def getDataType(self):
        """Returns the name of the data type for this attribute.

        Return:
        string

        """

        return 'String'