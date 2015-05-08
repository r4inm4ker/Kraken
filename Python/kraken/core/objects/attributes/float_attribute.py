"""Kraken - objects.Attributes.FloatAttribute module.

Classes:
FloatAttribute - Base Attribute.

"""

from kraken.core.objects.attributes.number_attribute import NumberAttribute
from kraken.core.kraken_system import ks


class FloatAttribute(NumberAttribute):
    """Float Attribute. Implemented value type checking and limiting."""

    def __init__(self, name, value=0.0, minValue=None, maxValue=None):
        super(FloatAttribute, self).__init__(name, value, minValue=minValue,
              maxValue=maxValue)

        assert type(self.value) in (int, float), "Value is not of type 'int' or 'float'."


    # ==============
    # Value Methods
    # ==============
    def getRTVal(self):
        """Returns and RTVal object for this attribute.

        Return:
        RTVal

        """
        return ks.rtVal('Scalar', self.value)


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
