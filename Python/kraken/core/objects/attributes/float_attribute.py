"""Kraken - objects.Attributes.FloatAttribute module.

Classes:
FloatAttribute - Base Attribute.

"""

from base_attribute import BaseAttribute


class FloatAttribute(BaseAttribute):
    """Float Attribute. Implemented value type checking and limiting."""

    __kType__ = "FloatAttribute"

    def __init__(self, name, value=0.0):
        super(FloatAttribute, self).__init__(name, value)
        if value == 0.0:
            self.setMax(1.0)
        else:
            self.setMax(value * 3.0)

        assert type(self.value) in (int, float), "Value is not of type 'int' or 'float'."


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