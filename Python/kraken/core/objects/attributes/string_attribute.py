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
        """Sets the value of the attribute..

        Args:
            value: Value to set the attribute to.

        Returns:
            bool: True if successful.

        """

        if not isinstance(value, basestring):
            raise TypeError("Value is not of type 'str':" + str(value))

        super(StringAttribute, self).setValue(str(value))

        return True


    def getRTVal(self):
        """Returns and RTVal object for this attribute.

        Returns:
            RTVal: RTVal object of the attribute.

        """

        return ks.rtVal('String', self._value)



    def getDataType(self):
        """Returns the name of the data type for this attribute.

        Note:
            This is a localized method specific to the String Attribute.

        Returns:
            str: String name of the attribute type.

        """

        return 'String'