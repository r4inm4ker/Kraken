"""Kraken - objects.Attributes.IntegerAttribute module.

Classes:
IntegerAttribute - Base Attribute.

"""

from kraken.core.objects.attributes.number_attribute import NumberAttribute
from kraken.core.kraken_system import ks


class IntegerAttribute(NumberAttribute):
    """Float Attribute. Implemented value type checking and limiting."""

    def __init__(self, name, value=0, minValue=None, maxValue=None, keyable=None, parent=None):
        super(IntegerAttribute, self).__init__(name, value=value, minValue=minValue,
              maxValue=maxValue, parent=parent)

        assert type(self._value) is int, "Value is not of type 'int'."


    # ==============
    # Value Methods
    # ==============
    def getRTVal(self):
        """Returns and RTVal object for this attribute.

        Returns:
            RTVal: RTVal object of the attribute.

        """

        return ks.rtVal('Integer', self._value)


    def validateValue(self, value):
        """Validates the incoming value is the correct type.

        Note:
            This is a localized method specific to the Integer Attribute.

        Args:
            value (int): value to check the type of.

        Returns:
            Boolean: True if valid.

        """

        if type(value) is not int:
            return False

        return True



    def getDataType(self):
        """Returns the name of the data type for this attribute.

        Note:
            This is a localized method specific to the Integer Attribute.

        Returns:
            str: String name of the attribute type.

        """

        return 'Integer'