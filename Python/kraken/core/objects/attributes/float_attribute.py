"""Kraken - objects.Attributes.FloatAttribute module.

Classes:
FloatAttribute - Base Attribute.

"""

from number_attribute import NumberAttribute
from kraken.core.kraken_system import ks

class FloatAttribute(NumberAttribute):
    """Float Attribute. Implemented value type checking and limiting."""

    def __init__(self, name, value=0.0, minValue=None, maxValue=None, keyable=None, lock=None, uiMin=None, uiMax=None):
        super(FloatAttribute, self).__init__(name, value, minValue=minValue, maxValue=maxValue, keyable=keyable, lock=lock, uiMin=uiMin, uiMax=uiMax)

        if minValue is None:
            if value < 0.0:
                self.setMin(value)
            else:
                self.setMin(0.0)

        if maxValue is None:
            if value == 0.0:
                self.setMax(1.0)
            else:
                self.setMax(value * 3.0)

        assert type(self._value) in (int, float), "Value is not of type 'int' or 'float'."


    def setValue(self, value):
        """Sets the value of the attribute.

        Arguments:
        value -- Value to set the attribute to.

        Return:
        True if successful.

        """

        if type(value) not in (int, float):
            raise TypeError("Value is not of type 'int' or 'float'.")

        if value < self._min:
            raise ValueError("Value is less than attribute minimum.")
        elif value > self._max:
            raise ValueError("Value is greater than attribute maximum.")

        super(FloatAttribute, self).setValue(value)

        return True


    def setUiMin(self, minimum):
        """Sets the default minimum ui slider value for the attribute.

        Note: Only works on float or integer attributes.

        Arguments:
        minimum -- float / integer, default minimum ui slider value.

        Return:
        True if successful.

        """

        assert type(self._value) in (int, float), "Value is not of type 'int' or 'float'."
        super(FloatAttribute, self).setUiMin(minimum)

        return True


    def setUiMax(self, maximum):
        """Sets the default maximum ui slider value for the attribute.

        Note: Only works on float or integer attributes.

        Arguments:
        maximum -- float / integer, default maximum ui slider value.

        Return:
        True if successful.

        """

        assert type(self._value) in (int, float), "Value is not of type 'int' or 'float'."
        super(FloatAttribute, self).setUiMax(maximum)

        return True


    def getRTVal(self):
        """Returns and RTVal object for this attribute.

        Return:
        RTVal

        """
        return ks.rtVal('Scalar', self._value)
