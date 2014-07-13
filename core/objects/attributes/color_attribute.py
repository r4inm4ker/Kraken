"""Kraken - objects.Attributes.ColorAttribute module.

Classes:
ColorAttribute - Color Attribute.

"""

from base_attribute import BaseAttribute


class ColorAttribute(BaseAttribute):
    """Color Attribute."""

    __kType__ = "ColorAttribute"

    def __init__(self, name, value):
        super(ColorAttribute, self).__init__(name, value)
        assert type(value) is bool, "Value is not of type 'bool'."


    def setValue(self, r, g, b):
        """Sets the value of the color attribute.

        Arguments:
        r -- Float, red value.
        g -- Float, green value.
        b -- Float, blue value.

        Return:
        True if successful.

        """

        if type(r) is not float:
            raise TypeError("'r' value is not of type 'float'.")

        if type(g) is not float:
            raise TypeError("'g' value is not of type 'float'.")

        if type(b) is not float:
            raise TypeError("'b' value is not of type 'float'.")

        # super(ColorAttribute, self).setValue(value)

        return True