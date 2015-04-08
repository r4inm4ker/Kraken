"""Kraken - objects.Attributes.FloatAttribute module.

Classes:
FloatAttribute - Base Attribute.

"""

from base_attribute import BaseAttribute
from kraken.core.kraken_system import ks


class FloatAttribute(BaseAttribute):
    """Float Attribute. Implemented value type checking and limiting."""

    __kType__ = "FloatAttribute"

    def __init__(self, name, value=0.0, minValue=0.0, maxValue=1.0):
        super(FloatAttribute, self).__init__(name, value)
        self.min = minValue
        self.max = maxValue

        assert type(self.value) in (int, float), "Value is not of type 'int' or 'float'."
        assert self.value >= self.min, "Value is less than attribute minimum."
        assert self.value <= self.max, "Value is greater than attribute maximum."


    def setValue(self, value):
        """Sets the value of the attribute.

        Arguments:
        value -- Value to set the attribute to.

        Return:
        True if successful.

        """

        if type(value) not in (int, float):
            raise TypeError("Value is not of type 'int' or 'float'.")

        if value < self.min:
            raise ValueError("Value is less than attribute minimum.")
        elif value > self.max:
            raise ValueError("Value is greater than attribute maximum.")

        super(FloatAttribute, self).setValue(value)

        return True

    def getRTVal(self):
        """Returns and RTVal object for this attribute.

        Return:
        RTVal

        """
        return ks.rtVal('Scalar', self.value)


        