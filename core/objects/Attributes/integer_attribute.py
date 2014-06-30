"""Kraken - objects.Attributes.IntegerAttribute module.

Classes:
IntegerAttribute - Base Attribute.

"""

from base_attribute import BaseAttribute


class IntegerAttribute(BaseAttribute):
    """Float Attribute. Implemented value type checking and limiting."""

    def __init__(self, name, value, minValue, maxValue):
        super(IntegerAttribute, self).__init__(name, value)
        self.min = minValue
        self.max = maxValue

        assert type(self.value) is int, "Value is not of type 'int'."
        assert self.value >= self.min, "Value is less than attribute minimum."
        assert self.value <= self.max, "Value is greater than attribute maximum."


    def setValue(self, value):
        """Ensures 'value' attribute is correct type and within min and max range."""

        if type(value) not in (int):
            raise TypeError("Value is not of type 'int'.")

        if value < self.min:
            raise ValueError("Value is less than attribute minimum.")
        elif value > self.max:
            raise ValueError("Value is greater than attribute maximum.")

        super(IntegerAttribute, self).setValue(value)

        return True