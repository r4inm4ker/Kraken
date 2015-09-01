"""Kraken - objects.Attributes.ScalarAttribute module.

Classes:
ScalarAttribute - Base Attribute.

"""

from kraken.core.objects.attributes.number_attribute import NumberAttribute
from kraken.core.kraken_system import ks


class ScalarAttribute(NumberAttribute):
    
    """Float Attribute. Implemented value type checking and limiting."""

    def __init__(self, name, value=0.0, minValue=None, maxValue=None, parent=None):
        super(ScalarAttribute, self).__init__(name, value=value, minValue=minValue,
              maxValue=maxValue, parent=parent)

        assert type(self._value) in (int, float), "Value is not of type 'int' or 'float'."


    # ==============
    # Value Methods
    # ==============
    def getRTVal(self):
        """Returns and RTVal object for this attribute.

        Return:
        RTVal

        """

        return ks.rtVal('Scalar', self._value)


    def validateValue(self, value):
        """Validates the incoming value is the correct type.

        Arguments:
        value -- Type, value to check the type of.

        Return:
        True if successful.

        """

        if type(value) not in (int, float):
            return False

        return True


    def getDataType(self):
        """Returns the name of the data type for this attribute.

        Return:
        string

        """

        return 'Scalar'