"""Kraken - objects.Attributes.IntegerAttribute module.

Classes:
IntegerAttribute - Base Attribute.

"""

from number_attribute import NumberAttribute


class IntegerAttribute(NumberAttribute):
    """Float Attribute. Implemented value type checking and limiting."""

    def __init__(self, name, value=0, minValue=None, maxValue=None):
        super(IntegerAttribute, self).__init__(name, value, minValue=minValue, maxValue=maxValue)

        if minValue is None:
            if value < 0:
                self.setMin(value)
            else:
                self.setMin(0)

        if maxValue is None:
            if value == 0:
                self.setMax(10)
            else:
                self.setMax(value * 3)

        assert type(self.value) is int, "Value is not of type 'int'."


    def setValue(self, value):
        """Sets the value of the attribute.

        Arguments:
        value -- Value to set the attribute to.

        Return:
        True if successful.

        """

        if type(value) not in (int):
            raise TypeError("Value is not of type 'int'.")

        if value < self.min:
            raise ValueError("Value is less than attribute minimum.")
        elif value > self.max:
            raise ValueError("Value is greater than attribute maximum.")

        super(IntegerAttribute, self).setValue(value)

        return True