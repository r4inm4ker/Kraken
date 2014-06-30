"""Kraken - objects.Attributes.BoolAttribute module.

Classes:
BoolAttribute - Base Attribute.

"""

from BaseAttribute import BaseAttribute


class BoolAttribute(BaseAttribute):
    """Boolean Attribute. Implemented value type checking and limiting."""

    def __init__(self, name, value):
        super(BoolAttribute, self).__init__(name, value)
        assert type(value) is bool, "Value is not of type 'bool'."


    def setValue(self, value):
        """Ensures 'value' attribute is correct type and within min and max range."""

        if type(value) is not bool:
            raise TypeError("Value is not of type 'bool'.")

        super(BoolAttribute, self).setValue(value)


        return True